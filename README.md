# vaud-rag

[![wakatime](https://wakatime.com/badge/user/4e37586b-a92c-445c-9c61-d6eecf04f9b7/project/8b3fe044-112c-4271-95dc-bbf5f7799813.svg)](https://wakatime.com/badge/user/4e37586b-a92c-445c-9c61-d6eecf04f9b7/project/8b3fe044-112c-4271-95dc-bbf5f7799813)

Proto RAG + MLflow sur les démarches chômage du canton de Vaud, construit en mode tutoriel guidé. Corpus officiel (vd.ch, ch.ch, Fedlex), citations des sources, abstention explicite quand l'information n'est pas trouvée, aucune conservation des questions des utilisateurs. Objectif : projet vitrine et expérience RAG + MLflow sur un cas réel.

> Navigation dans les documents officiels, pas un conseil juridique.

## Avancement

- [x] Config validée (YAML, `ValueError` si invalide)
- [x] Sitemap vd.ch (cache JSON, dédoublonnage)
- [x] Exploration des branches (`filter_urls` par segments, `group_by_branch`, `hit_ratio`)
- [x] Sélection par préfixes (`select_urls`, include/exclude en config)
- [x] Tests pytest : `group_by_branch`, `split_segments`, `filter_urls`, `select_urls`, `hit_ratio`
- [ ] robots.txt (Protego), téléchargement, extraction, filtres, staging
- [ ] Eval set, chunking, embeddings, retrieval, génération, MLflow, API

## Périmètre du corpus (V1)

Chômage uniquement : branche `economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/` (68 pages dans le sitemap au 2026-10-06, dont 31 rapports d'activité archivés exclus) et la page `prestation/obtenir-une-indemnite-en-cas-dinsolvabilite/`.
Les préfixes sont décidés à la main à partir de l'exploration (dans `config.yaml`), jamais écrits automatiquement.

## Cadre légal et conformité

Prévu et en cours d'implémentation (le crawler ne télécharge encore rien) :

- robots.txt de vd.ch lu et respecté par code (wildcards gérés via Protego, User-Agent identifiable, délai >= 1 s entre requêtes)
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
config/         config.yaml (une entrée par site), config.py (chargement, validation)
crawler/        crawler.py (sitemap, filtrage et sélection des URLs)
tests/          tests pytest (test_crawler.py)
conftest.py     fixtures partagées (urls)
pyproject.toml  configuration ruff (tabs) et pytest
.vscode/        réglages pytest/debug (local)
main.py         point d'entrée
```

## Décisions

- **Découverte / sélection / filtres séparés** : le crawler est générique, ce qui entre dans le corpus est décidé à la main dans `config.yaml` (préfixes de chemin), jamais réécrit par le programme.
- **Config validée au chargement** (`ValueError` explicite, pas de fallback silencieux).
- **Les fonctions lèvent, `main` décide** de quitter.
- **Code et logs en anglais**, corpus et eval set en français.
- **Indentation en tabs**, formatage via `ruff format`.
- **Fonctions pures testées unitairement** (URLs en dur dans les tests, jamais le vrai sitemap : pas de dépendance au réseau).
- **Classe `Crawler` repoussée** : introduite avec le téléchargement, quand il y aura un état de session à porter (Protego, User-Agent, délai).

## Observations sur vd.ch

- Sitemap en index paginé : 36 544 URLs brutes, 27 495 après dédoublonnage (doublons exacts, les mêmes pages listées dans plusieurs sous-sitemaps). Le total varie légèrement d'un parse à l'autre.
- Le Grand Conseil (`gc/seances-precedentes/`) représente environ la moitié du sitemap, hors périmètre.
- Branche chômage : `economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/`.
- robots.txt avec wildcards (`/*?cHash=*`), non géré par `urllib.robotparser` : Protego prévu.
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