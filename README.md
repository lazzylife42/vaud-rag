# vaud-rag

[![wakatime](https://wakatime.com/badge/user/4e37586b-a92c-445c-9c61-d6eecf04f9b7/project/8b3fe044-112c-4271-95dc-bbf5f7799813.svg)](https://wakatime.com/badge/user/4e37586b-a92c-445c-9c61-d6eecf04f9b7/project/8b3fe044-112c-4271-95dc-bbf5f7799813)

Proto RAG + MLflow sur les démarches chômage du canton de Vaud, construit en mode tutoriel guidé. Corpus officiel (vd.ch, ch.ch, Fedlex), citations des sources, abstention explicite quand l'information n'est pas trouvée, aucune conservation des questions des utilisateurs. Objectif : projet vitrine et expérience RAG + MLflow sur un cas réel.

> Navigation dans les documents officiels, pas un conseil juridique.

## Avancement

### Fait

- [x] Config validée (YAML, `ValueError` si invalide)
- [x] Sitemap vd.ch (cache JSON, dédoublonnage)
- [x] Exploration des branches (`filter_urls` par segments, `group_by_branch`, `hit_ratio`)
- [x] Sélection par préfixes (`select_urls`, include/exclude en config)
- [x] robots.txt avec Protego (`fetch_robots_text`, `parse_robots`, `is_allowed`, `sitemaps_from_robots`)
- [x] Module réseau, début : `compute_wait` (délai entre requêtes), contrat de données (`RobotsDisallowed`, `FetchError`, `FetchResult`), `check_allowed` (host strict puis robots.txt)
- [x] Tests pytest : `group_by_branch`, `split_segments`, `filter_urls`, `select_urls`, `hit_ratio`, `compute_wait`, `check_allowed`

### Reste à faire

- [ ] Module réseau : GET poli (délai, User-Agent, horodatage), redirections manuelles, garde-fous (content-type, taille max), assemblage en classe `PoliteFetcher`
- [ ] Sauvegarde du brut (`save_raw`), extraction du texte (trafilatura, canonical URL, hash du contenu), staging, run sur les pages sélectionnées
- [ ] Eval set, chunking, embeddings, retrieval, génération, MLflow, API

### Suite immédiate

Un GET poli : attendre `compute_wait`, envoyer le User-Agent, horodater en ISO 8601 UTC, retourner un `FetchResult`.

## Périmètre du corpus (V1)

Chômage uniquement : branche `economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/` (68 pages dans le sitemap au 2026-10-06, dont 31 rapports d'activité archivés exclus) et la page `prestation/obtenir-une-indemnite-en-cas-dinsolvabilite/`.
Les préfixes sont décidés à la main à partir de l'exploration (dans `config.yaml`), jamais écrits automatiquement.

## Cadre légal et conformité

Implémenté : lecture de robots.txt par code et contrôle de chaque URL (`check_allowed`). Le crawler ne télécharge encore aucune page. Prévu :

- robots.txt de vd.ch lu et respecté par code (wildcards gérés via Protego, User-Agent identifiable, délai entre requêtes : 2 s en config, 1 s minimum)
- Les communiqués de presse HTML ne sont pas interdits par le robots.txt (seul le dossier de fichiers `/fileadmin/user_upload/accueil/Communique_presse/` l'est) : ils sont exclus pour pertinence, pas pour des raisons de robots.txt
- vd.ch et ch.ch : droit d'auteur réservé. La démo ne republiera pas le texte des pages (embeddings + extrait court + lien vers la source)
- Fedlex (LACI, OACI) : texte non protégé (art. 5 LDA), indexable et citable
- Aucune question d'utilisateur n'est loggée ni stockée, pas d'IP, uniquement des compteurs agrégés
- Ce projet est une navigation dans les documents officiels, pas un conseil juridique

Non vérifié à ce stade : conditions d'utilisation d'arbeit.swiss, conditions du recueil cantonal (BLV), cadre LPD précis. Cette analyse n'est pas un avis juridique, seulement un point de départ.

## Limites connues

- Le filtre par mots-clés travaille sur le chemin de l'URL (segments exacts, `orp` ne matche plus `corporation`) : une page sans mot-clé dans son chemin n'est pas détectée, d'où la sélection par préfixes validée à la main
- Élisions (`lorp`, `demploi`) : ajoutées explicitement aux mots-clés, d'autres peuvent manquer
- Le ratio hits/total ne discrimine rien quand le nom de la branche contient déjà le mot-clé (toute la branche matche)
- Le sitemap évolue : le nombre d'URLs varie légèrement d'un parse à l'autre

## Structure

```
├── README.md
├── config
│   ├── config.py
│   └── config.yaml
├── conftest.py
├── crawler
│   ├── crawler.py
│   ├── fetcher.py
│   ├── robots.py
│   └── sitemap.json
├── main.py
├── pyproject.toml
├── requirements.txt
└── tests
    ├── test_crawler.py
    └── test_fetcher.py
```

## Décisions

- **Découverte / sélection / filtres séparés** : le crawler est générique, ce qui entre dans le corpus est décidé à la main dans `config.yaml` (préfixes de chemin), jamais réécrit par le programme.
- **Config validée au chargement** (`ValueError` explicite, pas de fallback silencieux).
- **Les fonctions lèvent, `main` décide** de quitter.
- **Code et logs en anglais**, corpus et eval set en français.
- **Indentation en tabs**, formatage via `ruff format`.
- **Fonctions pures testées unitairement** (URLs en dur dans les tests, jamais le vrai sitemap : pas de dépendance au réseau).
- **Classe `PoliteFetcher`** (remplace l'ancienne idée de classe `Crawler`) : elle portera l'état de session (User-Agent, Protego, délai, timestamp de la dernière requête, session HTTP). Le `Protego` est injecté, pas d'I/O dans `__init__`, `clock` et `sleeper` injectables pour tester sans attendre.
- **`check_allowed` juge une URL, jamais une réponse** : host d'abord (égalité stricte sur le hostname, `vd.ch` n'est pas `www.vd.ch`), puis robots.txt. URL sans host : `ValueError` (bug de l'appelant). Mauvais host ou chemin interdit : `RobotsDisallowed`.
- **Redirections suivies à la main** : robots vérifié avant chaque saut avec le même `Protego`, refus d'un changement de host, nombre de sauts limité.
- **Pas de retry en V1** : `FetchError` et log.
- **Séparation download / save_raw / extract** : brut dans `data/raw/<site>/<date_crawl>/<hash_url>.html`, texte nettoyé et métadonnées en JSON dans `data/staging/`.
- **Hash de détection de changement calculé sur le texte nettoyé**, pas sur le brut.

## Observations sur vd.ch

- Sitemap en index paginé : 36 544 URLs brutes, 27 495 après dédoublonnage (doublons exacts, les mêmes pages listées dans plusieurs sous-sitemaps). Le total varie légèrement d'un parse à l'autre.
- Le Grand Conseil (`gc/seances-precedentes/`) représente environ la moitié du sitemap, hors périmètre.
- Branche chômage : `economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/`.
- robots.txt avec wildcards (`/*?cHash=*`), non géré par `urllib.robotparser` : Protego utilisé.
- Filtrage par mots-clés : match par segments exacts, reste le trou des élisions.

## Données

`data/raw/`, `data/staging/`, `data/index/` et le cache du sitemap sont dans le `.gitignore` : le contenu de vd.ch / ch.ch n'est pas republié.

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
pytest -v
```