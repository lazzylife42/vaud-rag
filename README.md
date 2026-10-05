# vaud-rag

Proto RAG + MLflow sur les démarches chômage du canton de Vaud. Corpus officiel (vd.ch, ch.ch, Fedlex), citations, abstention, zéro log des questions. Projet tutoriel guidé, 2 semaines.

## Avancement

- [ ] **1. Ingestion**
  - [x] Découverte des URLs (sitemap)
  - [x] Config par site, validée strictement
  - [ ] Matching par segments + `explore` (proposition de préfixes)
  - [ ] Téléchargement (robots.txt via Protego, User-Agent, délai)
  - [ ] Extraction + filtres (langue, texte court, doublons)
- [ ] 2. Eval set
- [ ] 3. Chunking
- [ ] 4. Embeddings + index
- [ ] 5. Retrieval (dense, BM25, hybride, reranker)
- [ ] 6. Génération (citations, abstention)
- [ ] 7. MLflow
- [ ] 8. API + démo + README final

## Structure

```
config/    config.yaml (une entrée par site), config.py (chargement, validation)
crawler/   crawler.py (sitemap, filtrage des URLs)
main.py    point d'entrée
```

## Décisions

- **Découverte / sélection / filtres séparés** : le crawler est générique, ce qui entre dans le corpus est décidé à la main dans `config.yaml` (préfixes de chemin), jamais réécrit par le programme.
- **Config validée au chargement** (`ValueError` explicite, pas de fallback silencieux).
- **Les fonctions lèvent, `main` décide** de quitter.
- **Code et logs en anglais**, corpus et eval set en français.

## Observations sur vd.ch

- Sitemap en index paginé, ~36 500 URLs (2026-09-30).
- Branche chômage : `economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/`.
- robots.txt avec wildcards (`/*?cHash=*`), non géré par `urllib.robotparser` : Protego prévu.
- Filtrage par mots-clés : limites connues (sous-chaîne `orp`/`corporation`, élision `lorp`).

## Données

`data/` et le cache du sitemap ne sont pas versionnés : le contenu de vd.ch / ch.ch n'est pas republié.

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```