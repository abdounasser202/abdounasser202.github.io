from flask import Flask, render_template, abort, Response, redirect, url_for, request
from pathlib import Path
import hashlib
import json
import logging
from logging.handlers import RotatingFileHandler
import markdown
import os
import re
import sqlite3
import urllib.request
import yaml
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.debug = os.environ.get("FLASK_DEBUG", "0") == "1"

DATA_DIR = Path(__file__).parent / "data"
ARTICLES_DIR = Path(__file__).parent / "articles"
CANONICAL_HOST = "fandena.net"

# ---------------------------------------------------------------------------
# Logger ICS, sans identification d'infos personnelles (IP hashée), fichier rotatif
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ics_logger = logging.getLogger("ics_access")
ics_logger.setLevel(logging.INFO)
_ics_handler = RotatingFileHandler(
    LOG_DIR / "ics_access.log", maxBytes=10_000_000, backupCount=5
)
_ics_handler.setFormatter(logging.Formatter("%(asctime)s\t%(message)s"))
ics_logger.addHandler(_ics_handler)
ics_logger.propagate = False

# ---------------------------------------------------------------------------
# Capture email : stockage uniquement (alerte avant le prochain tournoi), pas de newsletter
# WAL : évite les locks entre workers gunicorn lors des écritures concurrentes
# ---------------------------------------------------------------------------
DB_DIR = Path(__file__).parent / "instance"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "emails.db"

_init_conn = sqlite3.connect(DB_PATH)
_init_conn.execute("PRAGMA journal_mode=WAL")
_init_conn.execute(
    "CREATE TABLE IF NOT EXISTS emails (email TEXT UNIQUE, created TEXT, source TEXT)"
)
_init_conn.commit()
_init_conn.close()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.context_processor
def inject_debug():
    return {"debug": app.debug}


@app.context_processor
def inject_tournaments():
    """Liste des tournois disponible dans TOUS les templates (sidebar + strip mobile)."""
    return {"tournaments": list_tournaments()}


OPENFOOTBALL_URL = (
    "https://cdn.jsdelivr.net/gh/openfootball/worldcup.json@master/2026/worldcup.json"
)
_live_cache = {"data": None, "ts": 0}
CACHE_TTL = 5 * 60  # secondes


# ---------------------------------------------------------------------------
# Drapeaux (zéro asset : émojis dérivés du code ISO 3166-1 alpha-2)
# ---------------------------------------------------------------------------

# Exceptions non-ISO (drapeaux régionaux Unicode)
SPECIAL_FLAGS = {
    "ENG": "🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f",  # gb-eng
    "SCO": "🏴\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f",  # gb-sct
    "WAL": "🏴\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f",  # gb-wls
}

# Codes FIFA (tels qu'utilisés dans nos JSON) → ISO 3166-1 alpha-2.
# Pièges connus : AUS = Autriche dans ce dataset (l'Australie utiliserait
# normalement AUS côté FIFA - à arbitrer si la source change), GER→DE,
# POR→PT, KSA→SA, CRO→HR, CAP→CV, COD→CD.
FIFA_TO_ISO2 = {
    # Hôtes
    "USA": "US",
    "CAN": "CA",
    "MEX": "MX",
    # Afrique
    "MAR": "MA",
    "SEN": "SN",
    "DZA": "DZ",
    "ALG": "DZ",
    "EGY": "EG",
    "CIV": "CI",
    "GHA": "GH",
    "TUN": "TN",
    "RSA": "ZA",
    "CAP": "CV",
    "COD": "CD",
    # Europe
    "FRA": "FR",
    "ESP": "ES",
    "POR": "PT",
    "GER": "DE",
    "NED": "NL",
    "BEL": "BE",
    "CRO": "HR",
    "NOR": "NO",
    "SUI": "CH",
    "AUS": "AT",  # Autriche dans ce dataset (voir note ci-dessus)
    "AUT": "AT",
    "ITA": "IT",
    "DEN": "DK",
    "POL": "PL",
    "SWE": "SE",
    "TUR": "TR",
    "UKR": "UA",
    "CZE": "CZ",
    "SVK": "SK",
    "ROU": "RO",
    "IRL": "IE",
    "ISL": "IS",
    "SRB": "RS",
    "GRE": "GR",
    "ALB": "AL",
    "MKD": "MK",
    "BIH": "BA",
    "KOS": "XK",
    "HUN": "HU",
    "SVN": "SI",
    # Amériques
    "ARG": "AR",
    "BRA": "BR",
    "URU": "UY",
    "COL": "CO",
    "ECU": "EC",
    "PAR": "PY",
    "CHL": "CL",
    "PER": "PE",
    "VEN": "VE",
    "BOL": "BO",
    "PAN": "PA",
    "CRC": "CR",
    "HON": "HN",
    "JAM": "JM",
    "HAI": "HT",
    "CUR": "CW",
    "SLV": "SV",
    # Asie / Océanie
    "JPN": "JP",
    "KOR": "KR",
    "IRN": "IR",
    "KSA": "SA",
    "QAT": "QA",
    "UZB": "UZ",
    "JOR": "JO",
    "IRQ": "IQ",
    "UAE": "AE",
    "NZL": "NZ",
}


def iso_flag(iso2):
    return "".join(chr(0x1F1E6 + ord(c) - 65) for c in iso2.upper())


def flag_of(code):
    """SPECIAL → dérivé ISO → '' (avec warning). Tournoi-agnostique : ne crashe jamais."""
    if code in SPECIAL_FLAGS:
        return SPECIAL_FLAGS[code]
    iso2 = FIFA_TO_ISO2.get(code)
    if iso2:
        return iso_flag(iso2)
    if len(code) == 3 and code.isalpha():
        logging.warning("no flag for %s", code)
    return ""


def is_placeholder_code(code):
    """Équipes non encore déterminées : '2A', 'W73', '3A/', 'L10'…"""
    return not (len(code) == 3 and code.isalpha())


def fetch_live_matches():
    """Fetche openfootball avec cache mémoire 5 min. Retourne la liste de matchs ou None."""
    now = datetime.now(timezone.utc).timestamp()
    if _live_cache["data"] is not None and now - _live_cache["ts"] < CACHE_TTL:
        return _live_cache["data"]
    try:
        with urllib.request.urlopen(OPENFOOTBALL_URL, timeout=3) as r:
            raw = json.loads(r.read())
        _live_cache["data"] = raw.get("matches", [])
        _live_cache["ts"] = now
        return _live_cache["data"]
    except Exception:
        return _live_cache["data"]  # stale ou None


def apply_live_data(t, live_matches):
    """Injecte date/heure/score depuis openfootball dans les matchs du tournoi."""
    if not live_matches:
        return
    # Index par (date, team1_en, team2_en)
    idx = {}
    for lm in live_matches:
        if not isinstance(lm.get("team1"), str):
            continue
        date = lm.get("date", "")
        idx[(date, lm["team1"], lm["team2"])] = lm
        idx[(date, lm["team2"], lm["team1"])] = lm

    for m in t["matches"]:
        date = m["kickoff_utc"][:10]
        t1 = m["team1"]["name_en"]
        t2 = m["team2"]["name_en"]
        lm = idx.get((date, t1, t2))
        if not lm:
            continue
        # Mise à jour du score dans la description (sera visible dans le .ics)
        if "score" in lm and isinstance(lm["score"].get("ft"), list):
            ft = lm["score"]["ft"]
            m["score_ft"] = ft  # utilisé plus bas si besoin
        # Mise à jour de l'heure si openfootball a une heure différente
        raw_time = lm.get("time", "")
        if raw_time and "UTC" in raw_time:
            try:
                time_part, offset_part = raw_time.split(" UTC")
                h, mn = map(int, time_part.split(":"))
                offset_h = int(offset_part) if offset_part else 0
                date_parts = [int(x) for x in date.split("-")]
                utc_dt = datetime(
                    date_parts[0],
                    date_parts[1],
                    date_parts[2],
                    h,
                    mn,
                    tzinfo=timezone.utc,
                ) - timedelta(hours=offset_h)
                m["kickoff_utc"] = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass


def load_tournament(slug):
    path = DATA_DIR / f"{slug}.json"
    if not path.exists():
        abort(404)
    t = json.loads(path.read_text(encoding="utf-8"))
    if slug == "cdm-2026":
        apply_live_data(t, fetch_live_matches())
    return t


def _article_slug(filename_stem):
    """Retire un éventuel préfixe numérique (ex: '01-mon-article' -> 'mon-article')."""
    return re.sub(r"^\d+-", "", filename_stem)


def _parse_article(path):
    raw = path.read_text(encoding="utf-8")
    _, front_matter, body = raw.split("---", 2)
    meta = yaml.safe_load(front_matter)
    html = markdown.markdown(body.strip(), extensions=["extra"])
    return {"meta": meta, "content": html}


def load_article(slug):
    """Charge un article SEO (frontmatter YAML + markdown) depuis articles/*.md, en ignorant un éventuel préfixe numérique du nom de fichier."""
    for path in ARTICLES_DIR.glob("*.md"):
        if _article_slug(path.stem) == slug:
            return _parse_article(path)
    return None


def list_articles():
    out = []
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        art = _parse_article(path)
        out.append({"slug": _article_slug(path.stem), **art["meta"]})
    return out


def list_tournaments():
    out = []
    for path in sorted(DATA_DIR.glob("*.json")):
        t = json.loads(path.read_text(encoding="utf-8"))
        out.append(
            {
                "id": t["id"],
                "name": t["name"],
                "short_name": t["short_name"],
                "start_date": t["start_date"],
                "end_date": t["end_date"],
            }
        )
    return out


def enrich_match(m, tz_name):
    """Ajoute local_dt, is_night, is_okhour, status à chaque match."""
    utc = datetime.fromisoformat(m["kickoff_utc"].replace("Z", "+00:00"))
    local = utc.astimezone(ZoneInfo(tz_name))
    now = datetime.now(timezone.utc)
    end = utc + timedelta(minutes=m.get("duration_min", 120))

    if now < utc:
        status = "upcoming"
    elif now < end:
        status = "live"
    else:
        status = "finished"

    return {
        **m,
        "local_dt": local,
        "is_night": local.hour < 7 or local.hour >= 23,
        # 13h–minuit pile, heure locale d'affichage (minuit pile OK, 00h01+ non)
        "is_okhour": (13 <= local.hour <= 23)
        or (local.hour == 0 and local.minute == 0),
        "status": status,
        "kickoff_utc_end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def is_choc(m, chocs):
    """True si la paire {t1,t2} est dans la liste de chocs."""
    pair = sorted([m["team1"]["code"], m["team2"]["code"]])
    return any(sorted(c) == pair for c in chocs)


@app.route("/")
def home():
    # Sidebar visible partout ; "/" redirige vers le premier tournoi (moins de code).
    ts = list_tournaments()
    if not ts:
        abort(404)
    return redirect(url_for("tournament", slug=ts[0]["id"]))


@app.route("/<slug>/")
def tournament(slug):
    t = load_tournament(slug)
    tz = t.get("tz_display", "Europe/Paris")
    chocs = t.get("chocs", [])
    fav_codes = {team["code"] for team in t.get("fav_teams", [])}
    kind_by_section = {s["id"]: s["kind"] for s in t["sections"]}

    matches = []
    for m in t["matches"]:
        em = enrich_match(m, tz)
        em["is_choc"] = is_choc(em, chocs)
        em["knockout"] = kind_by_section.get(em["section"]) == "knockout"
        for key in ("team1", "team2"):
            team = em[key]
            placeholder = is_placeholder_code(team["code"])
            em[key] = {
                **team,
                "flag": "" if placeholder else flag_of(team["code"]),
                "placeholder": placeholder,
                "fav": team["code"] in fav_codes,
            }
        matches.append(em)

    by_section = {}
    for s in t["sections"]:
        by_section[s["id"]] = {"meta": s, "matches": [], "teams_fr": None}
    for m in matches:
        by_section[m["section"]]["matches"].append(m)
    for _, data in by_section.items():
        if data["meta"]["kind"] == "group":
            seen = []
            for m in data["matches"]:
                for team in (m["team1"], m["team2"]):
                    if team["name_fr"] not in seen:
                        seen.append(team["name_fr"])
            data["teams_fr"] = seen

    return render_template(
        "tournament.html",
        t=t,
        sections=t["sections"],
        by_section=by_section,
        total_matches=len(matches),
    )


@app.route("/<slug>")
def article(slug):
    # Évite de casser l'ancien comportement (redirection 308 vers /<slug>/ pour un tournoi).
    if (DATA_DIR / f"{slug}.json").exists():
        return redirect(url_for("tournament", slug=slug), code=308)

    art = load_article(slug)
    if not art:
        abort(404)
    return render_template(
        "article.html", meta=art["meta"], content=art["content"], slug=slug
    )


@app.template_filter("format_day_fr")
def format_day_fr(dt):
    """datetime → 'Mar 16 juin'"""
    jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    mois = [
        "jan",
        "fév",
        "mar",
        "avr",
        "mai",
        "juin",
        "juil",
        "août",
        "sep",
        "oct",
        "nov",
        "déc",
    ]
    return f"{jours[dt.weekday()]} {dt.day} {mois[dt.month - 1]}"


@app.template_filter("gcal_url")
def gcal_url(m, t):
    from urllib.parse import urlencode

    title = f"⚽ {m['team1']['name_fr']} – {m['team2']['name_fr']} | {t['short_name']}"
    desc = f"{t['name']} - {m['section']}"
    start = m["kickoff_utc"].replace("-", "").replace(":", "").replace(".000Z", "Z")
    end_dt = datetime.fromisoformat(
        m["kickoff_utc"].replace("Z", "+00:00")
    ) + timedelta(minutes=m.get("duration_min", 120))
    end = end_dt.strftime("%Y%m%dT%H%M%SZ")
    params = {
        "action": "TEMPLATE",
        "text": title,
        "dates": f"{start}/{end}",
        "details": desc,
        "location": m["venue"],
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(params)


def build_ics(t):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//cdm2026//FR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{t['name']}",
        "X-PUBLISHED-TTL:PT12H",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
    ]
    now_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for m in t["matches"]:
        utc = datetime.fromisoformat(m["kickoff_utc"].replace("Z", "+00:00"))
        start_compact = utc.strftime("%Y%m%dT%H%M%SZ")
        end_dt = utc + timedelta(minutes=m.get("duration_min", 120))
        end_compact = end_dt.strftime("%Y%m%dT%H%M%SZ")
        title = (
            f"⚽ {m['team1']['name_fr']} – {m['team2']['name_fr']} | {t['short_name']}"
        )
        desc = f"{t['name']} - {m['section']}"
        lines += [
            "BEGIN:VEVENT",
            f"UID:{m['id']}@cdm2026",
            f"DTSTAMP:{now_stamp}",
            f"DTSTART:{start_compact}",
            f"DTEND:{end_compact}",
            f"SUMMARY:{title}",
            f"LOCATION:{m['venue']}",
            f"DESCRIPTION:{desc}",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)


@app.route("/<slug>/calendar.ics")
def calendar_ics(slug):
    t = load_tournament(slug)
    ics = build_ics(t)

    ua = request.headers.get("User-Agent", "-")
    ip_hash = hashlib.sha256((request.remote_addr or "").encode()).hexdigest()[:12]
    ics_logger.info(f"{slug}\t{ip_hash}\t{ua}")

    return Response(
        ics,
        mimetype="text/calendar; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{slug}.ics"',
            "Cache-Control": "public, max-age=3600",
        },
    )


@app.route("/subscribe", methods=["POST"])
def subscribe():
    # Honeypot : champ invisible (off-screen via CSS), un humain ne le remplit jamais.
    if request.form.get("website"):
        return {"ok": True}

    email = request.form.get("email", "").strip().lower()
    if not EMAIL_RE.match(email):
        return {"ok": False, "error": "invalid_email"}, 400

    source = request.form.get("source", "home")
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR IGNORE INTO emails (email, created, source) VALUES (?, ?, ?)",
        (email, created, source),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@app.route("/sitemap.xml")
def sitemap():
    lastmod = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for tour in list_tournaments():
        loc = f"https://{CANONICAL_HOST}/{tour['id']}/"
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")
    for art in list_articles():
        loc = f"https://{CANONICAL_HOST}/{art['slug']}"
        art_lastmod = str(art.get("date", lastmod))
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{art_lastmod}</lastmod></url>")
    lines.append("</urlset>")
    return Response(
        "\n".join(lines),
        mimetype="application/xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )


@app.route("/robots.txt")
def robots():
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: https://{CANONICAL_HOST}/sitemap.xml",
            "",
        ]
    )
    return Response(body, mimetype="text/plain")


@app.before_request
def redirect_legacy_host():
    host = request.host.split(":")[0]
    if host not in (CANONICAL_HOST, "localhost", "127.0.0.1"):
        return redirect(
            f"https://{CANONICAL_HOST}{request.full_path.rstrip('?')}", code=301
        )
