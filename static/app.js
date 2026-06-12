(function () {
  "use strict";

  var rows = Array.prototype.slice.call(document.querySelectorAll("li.match"));
  var cards = Array.prototype.slice.call(document.querySelectorAll("section.grp"));
  var teamChips = Array.prototype.slice.call(document.querySelectorAll(".chip-team"));
  var fChocs = document.getElementById("f-chocs");
  var fElims = document.getElementById("f-elims");
  var fOkhour = document.getElementById("f-okhour");
  var fReset = document.getElementById("f-reset");
  var countEl = document.getElementById("filter-count");
  var emptyEl = document.getElementById("empty-state");

  var nextUp = document.getElementById("next-up");
  var nuPrefix = nextUp ? nextUp.querySelector(".nu-prefix") : null;
  var nuTeams = nextUp ? nextUp.querySelector(".nu-teams") : null;
  var nuCountdown = nextUp ? nextUp.querySelector(".nu-countdown") : null;

  var toggles = [fChocs, fElims, fOkhour];

  if (!rows.length || !fChocs) return;

  var total = rows.length;

  // Pré-calcul des bornes temporelles de chaque ligne (ms epoch).
  rows.forEach(function (r) {
    var t = r.querySelector("time.m-hour");
    r._start = t ? Date.parse(t.getAttribute("datetime")) : NaN;
    r._end = r.dataset.end ? Date.parse(r.dataset.end) : r._start + 120 * 60000;
  });

  var visibleRows = [];

  function pressed(el) {
    return el.getAttribute("aria-checked") === "true";
  }

  function setPressed(el, v) {
    el.setAttribute("aria-checked", v ? "true" : "false");
  }

  function chipOn(el) {
    return el.getAttribute("aria-pressed") === "true";
  }

  function setChip(el, v) {
    el.setAttribute("aria-pressed", v ? "true" : "false");
  }

  // État par défaut : « Matchs de chocs » actif, le reste inactif, aucune chip.
  function isDefault() {
    return (
      pressed(fChocs) &&
      !pressed(fElims) &&
      !pressed(fOkhour) &&
      !teamChips.some(chipOn)
    );
  }

  // Équipes = base, toggles = raffineurs :
  //   sel = Set des codes chips actives ; C, E, H = chocs / élims / okhour
  //   inTeams(m) = sel.size == 0 ? true : (m.codes ∩ sel ≠ ∅)
  //   inCats(m)  = (!C && !E)    ? true : (C && m.choc) || (E && m.ko)
  //   visible(m) = inTeams(m) && inCats(m) && (!H || m.okhour)
  // On ne matche QUE sur data-codes, jamais sur la section ou le groupe.
  function apply() {
    var sel = {};
    var selSize = 0;
    teamChips.forEach(function (chip) {
      if (chipOn(chip)) {
        sel[chip.dataset.code] = true;
        selSize++;
      }
    });

    var C = pressed(fChocs);
    var E = pressed(fElims);
    var H = pressed(fOkhour);

    var shown = 0;
    rows.forEach(function (r) {
      var inTeams =
        selSize === 0 ||
        r.dataset.codes.split(",").some(function (c) { return sel[c]; });
      var inCats =
        (!C && !E) ||
        (C && r.dataset.choc === "1") ||
        (E && r.dataset.ko === "1");
      var vis = inTeams && inCats && (!H || r.dataset.okhour === "1");
      r.hidden = !vis;
      if (vis) shown++;
    });

    cards.forEach(function (card) {
      card.hidden = !card.querySelector("li.match:not([hidden])");
    });

    countEl.textContent = shown + " matchs affichés sur " + total;
    emptyEl.hidden = shown !== 0;
    fReset.hidden = isDefault();

    visibleRows = rows.filter(function (r) { return !r.hidden; });
    updateNextUp();
  }

  // ---- Bannière prochain match + badges dynamiques ----

  function clearDynTags(r) {
    var tags = r.querySelector(".m-tags");
    if (!tags) return;
    Array.prototype.slice
      .call(tags.querySelectorAll(".tag-live, .tag-next"))
      .forEach(function (e) { e.remove(); });
  }

  function addTag(r, cls, text) {
    var tags = r.querySelector(".m-tags");
    if (!tags) return;
    var s = document.createElement("span");
    s.className = "tag " + cls;
    s.textContent = text;
    tags.appendChild(s);
  }

  function pad(n) {
    return (n < 10 ? "0" : "") + n;
  }

  function fmtCountdown(ms) {
    var s = Math.max(0, Math.floor(ms / 1000));
    var d = Math.floor(s / 86400); s -= d * 86400;
    var h = Math.floor(s / 3600); s -= h * 3600;
    var m = Math.floor(s / 60); s -= m * 60;
    return (d > 0 ? "J-" + d + " " : "") + pad(h) + "h " + pad(m) + "min " + pad(s) + "s";
  }

  function updateNextUp() {
    if (!nextUp) return;
    var now = Date.now();
    var live = [];
    var next = null;

    visibleRows.forEach(function (r) {
      if (isNaN(r._start)) return;
      if (r._start <= now && now < r._end) {
        live.push(r);
      } else if (r._start > now && (!next || r._start < next._start)) {
        next = r;
      }
    });

    rows.forEach(clearDynTags);
    live.forEach(function (r) { addTag(r, "tag-live", "En cours"); });
    if (next) addTag(next, "tag-next", "Prochain");

    if (live.length) {
      var r = live[0];
      nextUp.classList.add("is-live");
      nuPrefix.textContent = "EN COURS : ";
      nuTeams.textContent = r.dataset.t1 + " – " + r.dataset.t2;
      nuCountdown.textContent = "";
      nextUp.hidden = false;
    } else if (next) {
      nextUp.classList.remove("is-live");
      nuPrefix.textContent = "Prochain match : ";
      nuTeams.textContent = next.dataset.t1 + " – " + next.dataset.t2;
      nuCountdown.textContent = "· " + fmtCountdown(next._start - now);
      nextUp.hidden = false;
    } else {
      nextUp.hidden = true;
    }
  }

  // ---- Câblage des contrôles ----

  teamChips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      setChip(chip, !chipOn(chip));
      apply();
    });
  });

  toggles.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setPressed(btn, !pressed(btn));
      apply();
    });
  });

  fReset.addEventListener("click", function () {
    // Réinitialiser = revenir à l'état par défaut (chocs uniquement).
    teamChips.forEach(function (c) { setChip(c, false); });
    setPressed(fChocs, true);
    setPressed(fElims, false);
    setPressed(fOkhour, false);
    apply();
  });

  // ---- Horaires dans le fuseau du navigateur (fallback SSR Paris) ----

  function localizeTimes() {
    var tz;
    try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return; }
    if (!tz || tz === "Europe/Paris") return;
    var dayFmt = new Intl.DateTimeFormat("fr-FR", { timeZone: tz, weekday: "short", day: "numeric", month: "short" });
    var hourFmt = new Intl.DateTimeFormat("fr-FR", { timeZone: tz, hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
    function part(parts, type) { for (var i = 0; i < parts.length; i++) { if (parts[i].type === type) return parts[i].value; } return ""; }
    document.querySelectorAll("li.match").forEach(function (row) {
      var timeEl = row.querySelector(".m-hour");
      if (!timeEl) return;
      var d = new Date(timeEl.getAttribute("datetime"));
      if (isNaN(d)) return;
      var day = dayFmt.format(d).replace(/\./g, "");
      day = day.charAt(0).toUpperCase() + day.slice(1);
      var dayEl = row.querySelector(".m-day");
      if (dayEl) dayEl.textContent = day;
      var parts = hourFmt.formatToParts(d);
      var h = parseInt(part(parts, "hour"), 10);
      var mn = part(parts, "minute");
      timeEl.textContent = (h < 10 ? "0" + h : "" + h) + "h" + mn;
      var night = h < 7 || h >= 23;
      var nuitEl = row.querySelector(".nuit");
      if (night && !nuitEl) {
        var tag = document.createElement("span");
        tag.className = "nuit";
        tag.textContent = "nuit";
        timeEl.parentNode.appendChild(tag);
      } else if (!night && nuitEl) { nuitEl.remove(); }
      var okhour = h >= 13 || (h === 0 && mn === "00");
      if (okhour) { row.setAttribute("data-okhour", "1"); } else { row.removeAttribute("data-okhour"); }
    });
    var city = tz.split("/").pop().replace(/_/g, " ");
    document.querySelectorAll(".tz-name").forEach(function (el) { el.textContent = "heure de " + city; });
  }

  // Réécrit les horaires + data-okhour AVANT le premier apply() (ordre critique).
  localizeTimes();

  // État par défaut au chargement : « Matchs de chocs » actif, le reste inactif.
  setPressed(fChocs, true);
  setPressed(fElims, false);
  setPressed(fOkhour, false);
  teamChips.forEach(function (c) { setChip(c, false); });
  apply();

  setInterval(updateNextUp, 1000);
})();


/*----------------------------------------
            CAPTURES EMAILS
------------------------------------------*/
(function () {
  "use strict";

  var form = document.getElementById("email-form");
  if (!form) return;

  var msg = document.getElementById("email-msg");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    msg.textContent = "";
    msg.className = "email-msg";

    fetch("/subscribe", { method: "POST", body: new FormData(form) })
      .then(function (r) {
        return r.json().then(function (data) {
          return { ok: r.ok, data: data };
        });
      })
      .then(function (res) {
        if (res.ok && res.data.ok) {
          msg.textContent = "Merci, c'est noté !";
          msg.className = "email-msg ok";
          form.reset();
          if (typeof gtag === "function") {
            gtag("event", "email_capture");
          }
        } else {
          msg.textContent = "Adresse invalide, vérifie et réessaie.";
          msg.className = "email-msg err";
        }
      })
      .catch(function () {
        msg.textContent = "Erreur réseau, réessaie plus tard.";
        msg.className = "email-msg err";
      });
  });
})();

/*----------------------------------------
            BANDEAU COOKIES
------------------------------------------*/
(function () {
  "use strict";

  var banner = document.getElementById("cookie-banner");
  if (!banner) return;

  var acceptBtn = document.getElementById("cookie-accept");
  var declineBtn = document.getElementById("cookie-decline");

  if (!localStorage.getItem("cookie_consent")) {
    banner.hidden = false;
  }

  acceptBtn.addEventListener("click", function () {
    localStorage.setItem("cookie_consent", "granted");
    banner.hidden = true;
    if (typeof gtag === "function") {
      gtag("consent", "update", { analytics_storage: "granted" });
    }
  });

  declineBtn.addEventListener("click", function () {
    localStorage.setItem("cookie_consent", "denied");
    banner.hidden = true;
  });
})();
