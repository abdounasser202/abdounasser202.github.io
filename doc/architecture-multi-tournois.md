ARCHITECTURE MULTI-TOURNOIS — PERFORMANCE & DONNÉES TEMPS RÉEL
================================================================

État actuel :
- Données par tournoi dans data/<slug>.json (chargé en mémoire à chaque
  requête).
- Scores : récupérés côté SERVEUR depuis openfootball + cache.
- 1 tournoi actif aujourd'hui (CDM 2026). Cible : 3–8 tournois à terme.


PHILOSOPHIE
-----------

À ton échelle (probablement <100k visites/mois hors tournoi, 10–500k
pendant), la majorité des "problèmes de perf" sont théoriques. Le vrai
risque n'est PAS la lenteur, c'est :

  1. Cache obsolète pendant un match live (score affiché en retard).
  2. Subscription ICS hammering ton serveur (Apple Calendar refetch
     toutes les ~15 min sur certaines configs).
  3. openfootball indisponible / changeant son schéma.
  4. Données historiques qui restent indexées mais dont personne ne se
     soucie (gaspillage si pas géré).

Le plan ci-dessous adresse ces 4 risques, dans cet ordre.


COMPRENDRE L'ÉCHELLE RÉELLE
---------------------------

Un tournoi typique :
- 50–150 matchs
- ~30 sections (groupes + phases finales)
- JSON brut : 30–80 KB
- En mémoire Python (dict parsé) : 200–500 KB

Pour 10 tournois en mémoire simultanément : ~5 MB max.
C'est négligeable. Un Flask en prod a typiquement 50–200 MB de baseline.

Conclusion : ne te casse pas la tête à "fragmenter" les JSON. Tout
charger en mémoire au démarrage est OK. Plus de soucis si un jour tu
arrives à 100 tournois (improbable avant des années).


STRATÉGIE DE CACHE DES SCORES (le sujet critique)
-------------------------------------------------

Tu as déjà : fetch côté serveur + cache. Bien. Maintenant la question
est : QUEL TTL ?

  Cas 1 : Aucun match live actuellement → TTL long (15–30 min).
  Cas 2 : Au moins 1 match live → TTL court (60–90 s).
  Cas 3 : Tournoi terminé (date_fin < today) → cache PERMANENT
          (pas de re-fetch, données finales gravées).

Implémentation conseillée (à intégrer dans app.py) :

    from time import time

    _scores_cache = {}   # { slug: { "data": [...], "ts": float, "ttl": int } }

    def get_scores(slug):
        t = load_tournament(slug)
        now = time()
        entry = _scores_cache.get(slug)
        if entry and now - entry["ts"] < entry["ttl"]:
            return entry["data"]

        # Décider du TTL en fonction du contexte
        if tournament_is_over(t):
            ttl = 60 * 60 * 24 * 7  # 7 jours (purement par sécurité)
        elif any_match_live(t):
            ttl = 60                # 1 min pendant un live
        else:
            ttl = 60 * 15           # 15 min sinon

        data = fetch_openfootball(slug)
        _scores_cache[slug] = {"data": data, "ts": now, "ttl": ttl}
        return data

Avantages :
- Sous le pic d'audience (mi-temps d'un gros match), tu ne demandes
  openfootball qu'une fois par minute, pas par utilisateur.
- Hors live, tu épargnes leurs serveurs et le tien.
- Tournoi terminé : ZÉRO fetch, le cache vit "à vie".


GESTION DES ABONNEMENTS ICS (le risque sous-estimé)
---------------------------------------------------

Quand un utilisateur s'abonne via webcal://, son client (Apple Calendar,
Google Calendar, Outlook) refetch ton URL :
- Apple Calendar : 5 min à 1h selon les versions (configurable, mais
  beaucoup de gens laissent 5 min).
- Google Calendar : ~12h (assez sage).
- Outlook : ~3h.

Si 5 000 utilisateurs s'abonnent à ton ICS, tu peux te prendre des
milliers de requêtes/heure SUR LE MÊME FICHIER. C'est gros.

Solutions à appliquer ENSEMBLE :

1. **ETag / Last-Modified** côté serveur.

       from flask import make_response
       import hashlib

       @app.route("/<slug>/calendar.ics")
       def calendar_ics(slug):
           t = load_tournament(slug)
           ics = build_ics(t)
           etag = hashlib.sha1(ics.encode()).hexdigest()

           if request.headers.get("If-None-Match") == etag:
               return ("", 304)

           resp = make_response(ics)
           resp.headers["Content-Type"] = "text/calendar; charset=utf-8"
           resp.headers["ETag"] = etag
           resp.headers["Cache-Control"] = "public, max-age=900"  # 15min
           return resp

   Un 304 ne renvoie pas le corps → quasi-zéro bande passante.

2. **Cache HTTP devant Flask** : si tu déploies en prod, mets nginx
   ou Cloudflare devant. Cache l'ICS pendant 5–15 min côté CDN.
   Économise 99% des hits à ton Flask.

3. **TTL de refresh explicite dans l'ICS** : déjà fait dans le prompt 27
   (X-PUBLISHED-TTL:PT12H + REFRESH-INTERVAL:VALUE=DURATION:PT12H).
   Tous les clients ne le respectent pas, mais beaucoup oui.


SCALER À PLUSIEURS TOURNOIS
---------------------------

PROBLÈME RÉEL #1 — Charger tous les JSON au démarrage ou à la demande ?

  Tu fais déjà à la demande (load_tournament(slug) à chaque requête).
  C'est OK jusqu'à ~50 tournois.

  Si tu veux optimiser : cache en mémoire les tournois avec invalidation
  sur mtime du fichier.

      _tournament_cache = {}   # { slug: { "data": ..., "mtime": float } }

      def load_tournament(slug):
          path = DATA_DIR / f"{slug}.json"
          if not path.exists():
              abort(404)
          mtime = path.stat().st_mtime
          entry = _tournament_cache.get(slug)
          if entry and entry["mtime"] == mtime:
              return entry["data"]
          data = json.loads(path.read_text(encoding="utf-8"))
          _tournament_cache[slug] = {"data": data, "mtime": mtime}
          return data

  Avantages : 0 I/O disque entre 2 modifications du fichier.
  Inconvénient : aucune complexité ajoutée.

PROBLÈME RÉEL #2 — Mappings openfootball par tournoi

  openfootball/worldcup.json suit le CDM. Pour la CAN, c'est un autre
  repo (openfootball/africa). Pour l'Euro, encore un autre.

  Solution : ajouter dans data/<slug>.json un champ :

      "scores_source": {
          "type": "openfootball",
          "url": "https://cdn.jsdelivr.net/gh/openfootball/africa@master/2027--africa-cup/cup.json"
      }

  Et dans app.py, fetch_openfootball() lit la source depuis le tournoi.

  Bonus : tu peux supporter PLUSIEURS sources (sofascore, footballapi.com)
  en mettant un type différent et un dispatcher.

PROBLÈME RÉEL #3 — Tournois terminés vs actifs

  Une fois CDM 2026 fini, sa page peut être :
  - servie en static (export HTML une fois pour toutes), ou
  - servie via Flask avec données figées (scores cache永continu).

  L'option statique est idéale pour les archives (zéro CPU, zéro fetch).

  Avec frozen-flask :

      pip install frozen-flask

      from flask_frozen import Freezer
      freezer = Freezer(app)

      @freezer.register_generator
      def tournament():
          for path in DATA_DIR.glob("*.json"):
              t = json.loads(path.read_text(encoding="utf-8"))
              if t.get("archived"):
                  yield {"slug": t["id"]}

      python -c "from app import freezer; freezer.freeze()"

  → génère un dossier build/ avec tout le HTML statique des tournois
  archivés. Tu le sers via nginx, Cloudflare Pages, GitHub Pages, etc.

  Les tournois actifs restent en Flask dynamique.


PROBLÈME RÉEL #4 — Indexation Google et URL canoniques

  Si tu as 5 tournois actifs/passés, structure :
  - / → liste des tournois (page d'accueil sobre)
  - /cdm-2026/ → calendrier CDM 2026
  - /can-2027/ → calendrier CAN 2027
  - /euro-2028/ → ...

  Met un <link rel="canonical"> sur chaque page.
  Ajoute un sitemap.xml généré depuis les data/*.json :

      @app.route("/sitemap.xml")
      def sitemap():
          urls = ["/"]
          for path in DATA_DIR.glob("*.json"):
              t = json.loads(path.read_text())
              urls.append(f"/{t['id']}/")
          # ... format XML
          return Response(xml_content, mimetype="application/xml")

  Et un /robots.txt qui pointe vers sitemap.xml.


PERFORMANCES OBSERVÉES À SURVEILLER
-----------------------------------

Une fois en prod, regarde toutes les semaines :

  1. **Hit rate du cache scores** : combien de fois /cdm-2026/ a servi
     du cache vs fetch openfootball.
     Cible : > 90 % de hits.

  2. **Latence p95 de la home et tournament page** : doit rester < 100ms
     server-side.

  3. **Taille de la réponse HTML** : ton minimalisme aide. Vise < 50 KB
     gzippé pour la page tournoi.

  4. **Bande passante ICS** : si elle explose, c'est que les clients
     refetch trop souvent. Forcer le Cache-Control: max-age=900 (15min)
     côté serveur les freine.


RÉSILIENCE FACE À openfootball
------------------------------

Que se passe-t-il si openfootball est down pendant la finale ?

  - Aujourd'hui : le serveur appelle openfootball, plante ou retourne []
    après timeout, l'utilisateur voit "Aucun match terminé".

  - Mieux : SI openfootball échoue, SERVIR LE DERNIER CACHE même s'il
    est expiré. Mieux des scores "vieux de 10 min" que pas de scores.

      def fetch_openfootball(slug, fallback_to_stale=True):
          try:
              # fetch normal
              ...
              return data
          except Exception:
              if fallback_to_stale and slug in _scores_cache:
                  return _scores_cache[slug]["data"]
              return []

  - Encore mieux : enregistrer chaque réponse réussie sur DISQUE
    (data/scores-cache/<slug>.json) pour survivre à un redémarrage.


CHECK-LIST AVANT LE PIC DE LA CDM
---------------------------------

[ ] TTL de cache scores adaptatif (live vs idle vs over) en place.
[ ] ETag + Cache-Control sur /<slug>/calendar.ics.
[ ] Fallback stale-cache si openfootball plante.
[ ] Logging minimal : combien de fetches openfootball/heure ?
[ ] Test charge basique : `wrk -t4 -c50 -d30s http://ton-app/cdm-2026/`
    doit tenir > 200 req/s sur un serveur 2 vCPU.
[ ] Tournoi archivable via frozen-flask testé sur un tournoi-jouet.
[ ] sitemap.xml en place.


RÈGLE D'OR
----------

À chaque ajout de fonctionnalité multi-tournois, te poser la question :
**est-ce que ça reste configurable via data/<slug>.json sans toucher au
code Python ?**

Si oui → bonne route.
Si non → repenser, sinon dans 3 tournois le code sera spaghetti.
