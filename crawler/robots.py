from urllib.parse import urljoin

import requests
from protego import Protego


def fetch_robots_text(base_url: str, user_agent: str) -> str:
	"""Télécharge le robots.txt du site avec le User-Agent donné (ValueError si échec réseau ou HTTP)."""
	headers = {}
	headers["User-Agent"] = user_agent
	url = urljoin(base_url, "robots.txt")
	try:
		r = requests.get(url=url, headers=headers, timeout=10)
		r.raise_for_status()
	except requests.exceptions.RequestException as e:
		raise ValueError(f"Cannot fetch {url}: {e}") from e
	return r.text


def parse_robots(robots_text: str) -> Protego:
	"""Parse le texte de robots.txt en objet Protego (ValueError si vide)."""
	if not robots_text.strip():
		raise ValueError("Can't parse an empty string.")
	return Protego.parse(robots_text)


def is_allowed(rp: Protego, url: str, user_agent: str) -> bool:
	"""Indique si le User-Agent peut récupérer l'URL selon robots.txt."""
	return rp.can_fetch(url, user_agent)


def sitemaps_from_robots(rp: Protego) -> list[str]:
	"""Liste les sitemaps déclarés dans robots.txt."""
	return list(rp.sitemaps)
