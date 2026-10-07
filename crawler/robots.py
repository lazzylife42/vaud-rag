import requests
from urllib.parse import urljoin
from protego import Protego


def fetch_robots_text(base_url: str, user_agent: str) -> str:
	headers = {}
	headers["User-Agent"] = user_agent
	url = urljoin(base_url, "robots.txt")
	try:
		r = requests.get(url=url, headers=headers, timeout=2)
		r.raise_for_status()
	except requests.exceptions.RequestException as e:
		raise ValueError(f"Cannot fetch {url}: {e}") from e
	return r.text


def parse_robots(robots_text: str) -> Protego:
	if not robots_text.strip():
		raise ValueError("Can't parse an empty string.")
	return Protego.parse(robots_text)


def is_allowed(rp: Protego, url: str, user_agent: str) -> bool:
	return rp.can_fetch(url, user_agent)


def sitemaps_from_robots(rp: Protego) -> list[str]:
	return list(rp.sitemaps)
