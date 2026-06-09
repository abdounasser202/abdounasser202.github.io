from flask import Flask, render_template, abort, Response, redirect, url_for
from pathlib import Path
import json
import os
import urllib.request
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.debug = os.environ.get("FLASK_DEBUG", "0") == "1"
DATA_DIR = Path(__file__).parent / "data"

@app.context_processor
def inject_debug():
    return {"debug": app.debug}

OPENFOOTBALL_URL = (
    "https://cdn.jsdelivr.net/gh/openfootball/worldcup.json@master/2026/worldcup.json"
)
_live_cache = {"data": None, "ts": 0}
CACHE_TTL = 5 * 60  # secondes 


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
    """Ajoute local_dt, is_night, status à chaque match."""
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
        "status": status,
        "kickoff_utc_end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def is_choc(m, chocs):
    """True si la paire {t1,t2} est dans la liste de chocs."""
    pair = sorted([m["team1"]["code"], m["team2"]["code"]])
    return any(sorted(c) == pair for c in chocs)


@app.route("/")
def home():
    # return render_template("home.html", tournaments=list_tournaments())
    return redirect(url_for("tournament", slug="cdm-2026"))


@app.route("/<slug>/")
def tournament(slug):
    t = load_tournament(slug)
    tz = t.get("tz_display", "Europe/Paris")
    chocs = t.get("chocs", [])
    flags = {team["code"]: team.get("flag", "") for team in t.get("fav_teams", [])}

    matches = []
    for m in t["matches"]:
        em = enrich_match(m, tz)
        em["is_choc"] = is_choc(em, chocs)
        for key in ("team1", "team2"):
            em[key] = {**em[key], "flag": flags.get(em[key]["code"], "")}
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


@app.template_filter("dtformat_ics")
def dtformat_ics(dt):
    """'2026-06-13T22:00:00Z' → '20260613T220000Z'"""
    if isinstance(dt, str):
        return dt.replace("-", "").replace(":", "").split(".")[0]
    return dt.strftime("%Y%m%dT%H%M%SZ")


@app.template_filter("format_date_fr")
def format_date_fr(dt):
    """datetime → 'Sam 14 juin · 00h00'"""
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
    return (
        f"{jours[dt.weekday()]} {dt.day} {mois[dt.month - 1]} · {dt.strftime('%Hh%M')}"
    )


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
    return Response(
        ics,
        mimetype="text/calendar; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{slug}.ics"',
            "Cache-Control": "public, max-age=3600",
        },
    )


if __name__ == "__main__":
    app.run(debug=True)
