from dataclasses import dataclass


class RobotsDisallowed(Exception):
	"""URL interdite par robots.txt (ou hors du host autorisé)."""


class FetchError(Exception):
	"""Échec du téléchargement (réseau, statut HTTP, type ou taille inattendus)."""


@dataclass(frozen=True)
class FetchResult:
	"""Réponse téléchargée : URL demandée et finale, statut, type, corps brut, date UTC."""
	url: str
	final_url: str
	status: int
	content_type: str
	body: bytes
	fetched_at: str


def compute_wait(last_request: float | None, now: float, delay: float) -> float:
	"""Secondes restantes à attendre (0.0 si délai écoulé ou première requête)."""
	if delay < 0.0:
		raise ValueError("delay param can't be negative.")
	if last_request is None:
		return 0.0
	delta = now - last_request
	if delta >= 0.0 and (delay - delta) > 0.0:
		return delay - delta
	return 0.0
