            // ---- Scores live depuis openfootball ----
            const SCORES_URL =
                "https://cdn.jsdelivr.net/gh/openfootball/worldcup.json@master/2026/worldcup.json";
            const CACHE_KEY = "cdm2026-scores";
            const CACHE_TTL = 5 * 60 * 1000;

            async function loadScores() {
                try {
                    const c = sessionStorage.getItem(CACHE_KEY);
                    if (c) {
                        const o = JSON.parse(c);
                        if (
                            Date.now() - o.ts < CACHE_TTL &&
                            Array.isArray(o.data)
                        )
                            return o.data;
                    }
                } catch (e) {}
                try {
                    const r = await fetch(SCORES_URL, { cache: "no-cache" });
                    if (!r.ok) throw new Error("HTTP " + r.status);
                    const json = await r.json();
                    const data = json.matches || [];
                    try {
                        sessionStorage.setItem(
                            CACHE_KEY,
                            JSON.stringify({ ts: Date.now(), data }),
                        );
                    } catch (e) {}
                    return data;
                } catch (e) {
                    console.warn(e);
                    return null;
                }
            }

            function applyScores(apiMatches) {
                const st = document.getElementById("score-status");
                if (!apiMatches) {
                    st.innerHTML =
                        '<span class="score-status err">Scores indisponibles (openfootball injoignable). <a href="#" id="retry">Réessayer</a>.</span>';
                    const r = document.getElementById("retry");
                    if (r)
                        r.addEventListener("click", async function (e) {
                            e.preventDefault();
                            sessionStorage.removeItem(CACHE_KEY);
                            st.textContent = "Chargement des scores…";
                            const d = await loadScores();
                            applyScores(d);
                        });
                    return;
                }
                let nb = 0;
                document.querySelectorAll("li[data-mid]").forEach((li) => {
                    const date = li.dataset.date;
                    const t1 = li.dataset.t1;
                    const t2 = li.dataset.t2;
                    let api = apiMatches.find(
                        (x) =>
                            x.date === date &&
                            ((x.team1 === t1 && x.team2 === t2) ||
                                (x.team1 === t2 && x.team2 === t1)),
                    );
                    if (!api) {
                        api = apiMatches.find(
                            (x) =>
                                x.date === date &&
                                (x.team1 === t1 ||
                                    x.team2 === t1 ||
                                    x.team1 === t2 ||
                                    x.team2 === t2),
                        );
                    }
                    if (!api || !api.score || !Array.isArray(api.score.ft))
                        return;
                    const [a, b] = api.score.ft;
                    let h, aw;
                    if (api.team1 === t1) {
                        h = a;
                        aw = b;
                    } else if (api.team1 === t2) {
                        h = b;
                        aw = a;
                    } else {
                        h = a;
                        aw = b;
                    }
                    const sv = li.querySelector(".score-val");
                    if (sv) {
                        sv.className = "score-val";
                        sv.textContent = h + " – " + aw;
                        nb++;
                    }
                });
                st.innerHTML =
                    nb > 0
                        ? '<span class="score-status">' +
                          nb +
                          " score" +
                          (nb > 1 ? "s" : "") +
                          " chargé" +
                          (nb > 1 ? "s" : "") +
                          " depuis openfootball.</span>"
                        : '<span class="score-status">Aucun match terminé pour l\'instant - les scores apparaîtront ici automatiquement.</span>';
            }

            // ---- Filtre de recherche + filtres équipes ----
            function escHtml(s) {
                return s.replace(
                    /[&<>"']/g,
                    (c) =>
                        ({
                            "&": "&amp;",
                            "<": "&lt;",
                            ">": "&gt;",
                            '"': "&quot;",
                            "'": "&#39;",
                        })[c],
                );
            }

            function isChoc(li) {
                return li.dataset.choc === "1";
            }

            function isGroupStage(li) {
                return (li.dataset.section || "").startsWith("Group");
            }

            function isReasonableTime(li) {
                const s = li.dataset.start;
                if (!s) return true;
                const h = parseInt(s.substring(9, 11), 10);
                const m = parseInt(s.substring(11, 13), 10);
                // Paris is UTC+2 (CEST during tournament)
                const parisMinutes = (h * 60 + m + 120) % 1440;
                return parisMinutes >= 780 && parisMinutes < 1440;
            }

            function getSelectedChips() {
                const s = new Set();
                document.querySelectorAll('#chips .chip[aria-pressed="true"]').forEach((c) => s.add(c.dataset.team));
                return s;
            }

            function addChocBadges() {
                document.querySelectorAll("li[data-mid]").forEach((li) => {
                    if (!isChoc(li)) return;
                    const existing = li.querySelector(".choc-badge");
                    if (existing) return;
                    const badge = document.createElement("span");
                    badge.className = "choc-badge";
                    badge.innerHTML =
                        '<svg class="choc-icon" viewBox="0 0 24 24" width="12" height="12" aria-hidden="true">' +
                        '<path d="M13 2 4 14h6l-1 8 9-12h-6z" fill="currentColor"/></svg>CHOC';
                    const actions = li.querySelector(".actions");
                    if (actions) actions.appendChild(badge);
                    else li.appendChild(badge);
                });
            }

            let searchQuery = "";

            function applyFilters() {
                const fMesEquipes = document.getElementById("f-mes-equipes").checked;
                const fChocs = document.getElementById("f-chocs").checked;
                const fHoraire = document.getElementById("f-horaire").checked;
                const fEliminatoires = document.getElementById("f-eliminatoires").checked;
                const selectedTeams = getSelectedChips();
                const q = searchQuery.trim().toLowerCase();

                // Are any inclusive "show me X" sources turned on at all?
                const anySource =
                    (fMesEquipes && selectedTeams.size > 0) || fChocs || fEliminatoires;

                let visible = 0;
                document.querySelectorAll("li[data-mid]").forEach((li) => {
                    const group = isGroupStage(li);

                    // A match is included if at least one source asks for it.
                    const fromMyTeams = fMesEquipes && group &&
                        (selectedTeams.has(li.dataset.t1) || selectedTeams.has(li.dataset.t2));
                    const fromChocs = fChocs && isChoc(li);
                    const fromElim = fEliminatoires && !group;

                    let show = fromMyTeams || fromChocs || fromElim;

                    // "Heures raisonnables" narrows the active sources, but acts
                    // as a source on its own when nothing else is selected.
                    if (fHoraire) {
                        show = anySource
                            ? show && isReasonableTime(li)
                            : isReasonableTime(li);
                    }
                    if (q) show = show && li.textContent.toLowerCase().includes(q);

                    li.style.display = show ? "" : "none";
                    if (show) visible++;
                });

                document.querySelectorAll("main section.grp").forEach((sec) => {
                    const any =
                        sec.querySelectorAll(
                            'li[data-mid]:not([style*="display: none"])',
                        ).length > 0;
                    sec.style.display = any ? "" : "none";
                });

                const emptyState = document.getElementById("empty-state");
                const noFilter = !fChocs && !fEliminatoires && !fHoraire &&
                                 (!fMesEquipes || selectedTeams.size === 0);
                if (emptyState) {
                    if (visible === 0 && !q) {
                        emptyState.style.display = "";
                        const p = emptyState.querySelector("p");
                        if (p) {
                            if (fMesEquipes && selectedTeams.size === 0) {
                                p.textContent =
                                    "Tu as activé « Mes équipes » mais aucune équipe n'est sélectionnée. " +
                                    "Clique sur un drapeau au-dessus pour choisir ton équipe.";
                            } else if (noFilter) {
                                p.textContent =
                                    "Choisis au moins une option ci-dessus : équipes favorites, " +
                                    "matchs de chocs, ou phases éliminatoires.";
                            } else {
                                p.textContent =
                                    "Aucun match ne correspond à tes filtres. Essaie d'élargir " +
                                    "tes critères (par exemple décocher « horaire raisonnable »).";
                            }
                        }
                    } else {
                        emptyState.style.display = "none";
                    }
                }

                const fc = document.getElementById("filter-count");
                if (fc) {
                    const reset = document.getElementById("reset-filters");
                    const filtered = visible < 60;
                    fc.className = "filter-count" + (filtered ? " active" : "");
                    fc.firstChild.textContent =
                        visible + " match" + (visible > 1 ? "s" : "") +
                        " affiché" + (visible > 1 ? "s" : "") + " sur 60 · ";
                    if (reset) reset.style.display = filtered ? "" : "none";
                }

                const meta = document.getElementById("meta");
                if (q) {
                    meta.innerHTML =
                        visible === 0
                            ? "Aucun match ne correspond à « " +
                              escHtml(q) +
                              ' ». <a href="#" class="clear-link">Effacer</a>.'
                            : visible +
                              " match" +
                              (visible > 1 ? "s" : "") +
                              " affiché" +
                              (visible > 1 ? "s" : "") +
                              ' · <a href="#" class="clear-link">Effacer</a>';
                    const cl = meta.querySelector(".clear-link");
                    if (cl)
                        cl.addEventListener("click", function (e) {
                            e.preventDefault();
                            document.getElementById("q").value = "";
                            searchQuery = "";
                            applyFilters();
                        });
                } else {
                    meta.textContent = "60 matchs au total";
                }

                writeUrlState();
                updateLiveNextBadges();
                updateNextUp();
            }

            // ---- URL state sync ----

            function readUrlState() {
                const u = new URL(window.location.href);
                const teams = (u.searchParams.get("teams") || "").split(",").filter(Boolean);
                const fMesEquipes = teams.length > 0;
                const fChocs = u.searchParams.get("chocs") === "1";
                const fHoraire = u.searchParams.get("horaire") === "1";
                const fElim = u.searchParams.get("elim") === "1";
                const q = u.searchParams.get("q") || "";

                const hasAny = u.searchParams.has("teams") ||
                               u.searchParams.has("chocs") ||
                               u.searchParams.has("horaire") ||
                               u.searchParams.has("elim") ||
                               u.searchParams.has("q");
                if (!hasAny) return null;

                return { teams, fMesEquipes, fChocs, fHoraire, fElim, q };
            }

            function writeUrlState() {
                const teams = [...document.querySelectorAll('#chips .chip[aria-pressed="true"]')]
                    .map(c => c.dataset.team);
                const u = new URL(window.location.href);
                const sp = u.searchParams;

                teams.length ? sp.set("teams", teams.join(",")) : sp.delete("teams");
                document.getElementById("f-chocs").checked ? sp.set("chocs", "1") : sp.delete("chocs");
                document.getElementById("f-horaire").checked ? sp.set("horaire", "1") : sp.delete("horaire");
                document.getElementById("f-eliminatoires").checked ? sp.set("elim", "1") : sp.delete("elim");
                searchQuery.trim() ? sp.set("q", searchQuery.trim()) : sp.delete("q");

                history.replaceState(null, "", u.pathname + (sp.toString() ? "?" + sp.toString() : ""));
            }

            // ---- Live / next badges ----

            function parseStart(s) {
                const y = s.slice(0,4), M = s.slice(4,6), d = s.slice(6,8);
                const h = s.slice(9,11), m = s.slice(11,13);
                return Date.parse(`${y}-${M}-${d}T${h}:${m}:00Z`);
            }

            function formatCountdown(deltaMs) {
                if (deltaMs <= 0) return "";
                const totalMin = Math.floor(deltaMs / 60000);
                const days  = Math.floor(totalMin / (60 * 24));
                const hours = Math.floor((totalMin % (60 * 24)) / 60);
                const mins  = totalMin % 60;
                if (days > 0)  return `dans ${days}j ${hours}h`;
                if (hours > 0) return `dans ${hours}h ${mins}min`;
                return `dans ${mins}min`;
            }

            function updateNextUp() {
                const el = document.getElementById("next-up");
                if (!el) return;

                const selected = getSelectedChips();
                if (selected.size === 0) { el.hidden = true; return; }

                const now = Date.now();
                const candidates = [...document.querySelectorAll("li[data-mid]")]
                    .filter(li => selected.has(li.dataset.t1) || selected.has(li.dataset.t2))
                    .map(li => ({
                        start: parseStart(li.dataset.start),
                        end:   parseStart(li.dataset.end),
                        teams: li.querySelector(".teams").textContent.trim(),
                    }))
                    .filter(x => x.end > now)
                    .sort((a, b) => a.start - b.start);

                if (candidates.length === 0) { el.hidden = true; return; }

                const next = candidates[0];
                const live = now >= next.start && now < next.end;
                el.hidden = false;
                el.classList.toggle("live", live);
                el.innerHTML = live
                    ? `● <strong>${next.teams}</strong> <span class="countdown">en cours</span>`
                    : `Prochain match : <strong>${next.teams}</strong> <span class="countdown">${formatCountdown(next.start - now)}</span>`;
            }

            function updateLiveNextBadges() {
                const now = Date.now();
                let nextSet = false;

                document.querySelectorAll(".live-badge, .next-badge")
                        .forEach(b => b.remove());

                const items = [...document.querySelectorAll("li[data-mid]")]
                    .filter(li => li.style.display !== "none");

                items.forEach(li => {
                    const start = parseStart(li.dataset.start);
                    const end   = parseStart(li.dataset.end);
                    const actions = li.querySelector(".actions");
                    if (!actions) return;

                    if (now >= start && now < end) {
                        const b = document.createElement("span");
                        b.className = "live-badge";
                        b.textContent = "● EN COURS";
                        actions.appendChild(b);
                    } else if (!nextSet && start > now) {
                        const b = document.createElement("span");
                        b.className = "next-badge";
                        b.textContent = "→ PROCHAIN";
                        actions.appendChild(b);
                        nextSet = true;
                    }
                });
            }

            function updateMatchStatuses() {
                const now = Date.now();
                document.querySelectorAll("li[data-mid]").forEach(li => {
                    const start = parseStart(li.dataset.start);
                    const end   = parseStart(li.dataset.end);
                    let status = "upcoming";
                    if (now >= start && now < end) status = "live";
                    else if (now >= end)           status = "finished";
                    li.dataset.status = status;
                });
            }

            function updateFilterBarScrolled() {
                const bar = document.getElementById("filter-bar");
                if (!bar) return;
                if (window.scrollY > 200) bar.classList.add("scrolled");
                else bar.classList.remove("scrolled");
            }

            let scrollPending = false;
            window.addEventListener("scroll", () => {
                if (scrollPending) return;
                scrollPending = true;
                requestAnimationFrame(() => {
                    updateFilterBarScrolled();
                    scrollPending = false;
                });
            }, { passive: true });

            setInterval(updateLiveNextBadges, 60_000);
            setInterval(updateNextUp, 60_000);
            setInterval(updateMatchStatuses, 60_000);

            document
                .getElementById("q")
                .addEventListener("input", (e) => {
                    searchQuery = e.target.value;
                    applyFilters();
                });

            // ---- Init ----
            loadScores().then(applyScores);

            addChocBadges();
            updateMatchStatuses();
            updateLiveNextBadges();
            updateNextUp();

            document.querySelectorAll("#chips .chip").forEach((chip) => {
                chip.addEventListener("click", () => {
                    const pressed = chip.getAttribute("aria-pressed") === "true";
                    chip.setAttribute("aria-pressed", String(!pressed));
                    applyFilters();
                });
            });

            ["f-mes-equipes", "f-chocs", "f-horaire", "f-eliminatoires"].forEach((id) => {
                document.getElementById(id).addEventListener("change", () => {
                    const chipsRow = document.getElementById("chips");
                    if (id === "f-mes-equipes") {
                        chipsRow.style.display =
                            document.getElementById("f-mes-equipes").checked ? "" : "none";
                    }
                    applyFilters();
                });
            });

            document.getElementById("toggle-all-matches").addEventListener("click", (e) => {
                e.preventDefault();
                document.getElementById("f-mes-equipes").checked = true;
                document.getElementById("f-eliminatoires").checked = true;
                document.querySelectorAll("#chips .chip").forEach((c) => c.setAttribute("aria-pressed", "true"));
                document.getElementById("chips").style.display = "";
                applyFilters();
            });

            document.getElementById("reset-filters").addEventListener("click", (e) => {
                e.preventDefault();
                document.getElementById("f-mes-equipes").checked = false;
                document.getElementById("f-chocs").checked = true;
                document.getElementById("f-horaire").checked = false;
                document.getElementById("f-eliminatoires").checked = false;
                document.getElementById("chips").style.display = "none";
                document.querySelectorAll("#chips .chip").forEach((c) => c.setAttribute("aria-pressed", "false"));
                searchQuery = "";
                document.getElementById("q").value = "";
                applyFilters();
            });

            const initial = readUrlState();
            if (initial) {
                document.getElementById("f-mes-equipes").checked = initial.fMesEquipes;
                document.getElementById("f-chocs").checked = initial.fChocs;
                document.getElementById("f-horaire").checked = initial.fHoraire;
                document.getElementById("f-eliminatoires").checked = initial.fElim;
                document.getElementById("chips").style.display = initial.fMesEquipes ? "" : "none";
                document.querySelectorAll("#chips .chip").forEach(c => {
                    c.setAttribute("aria-pressed", initial.teams.includes(c.dataset.team) ? "true" : "false");
                });
                document.getElementById("q").value = initial.q;
                searchQuery = initial.q;
            }

            applyFilters();
