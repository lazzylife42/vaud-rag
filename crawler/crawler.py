import re
import json
import logging
from collections import Counter
from urllib.parse import urlsplit
from trafilatura import sitemaps


def get_sitemap(url: str) -> list[str]:
	sitemap_path = "./crawler/sitemap.json"
	try:
		with open(sitemap_path, "r", encoding="utf-8") as f:
			sitemap = json.load(f)

	except FileNotFoundError:
		logging.warning(
			'File "sitemap.json" not found. Trying to parse it from BASE_URL.'
		)
		sitemap = list(dict.fromkeys(sitemaps.sitemap_search(url=url)))
		with open(sitemap_path, "w", encoding="utf-8") as f:
			json.dump(sitemap, f, indent=4)

	logging.info(f"Sitemap contains {len(sitemap)} urls.")
	return sitemap


def group_by_branch(urls: list[str], depth: int = 3) -> Counter:
	if depth < 1:
		raise ValueError("depth must be >= 1.")
	counter = Counter()
	for url in urls:
		path = urlsplit(url).path.strip("/")
		if not path:
			continue
		niveaux = path.strip("/").split("/")
		key = "/".join(niveaux[:depth]) + "/"
		counter[key] += 1
	return counter


def hit_ratio(total: Counter, hits: Counter) -> list[tuple[str, int, int, float]]:
	rows = []
	for key in hits:
		if total[key] == 0:
			raise ValueError("total key can't be zero.")
		rows.append((key, hits[key], total[key], hits[key] / total[key]))

	rows.sort(key=lambda row: row[3], reverse=True)
	return rows


def split_segments(url: str) -> list[str]:
	path = urlsplit(url.lower()).path
	return [token for token in re.split(r"[-/]", path) if token]


def select_urls(
	sitemap: list[str], include: list[str], exclude: list[str]
) -> list[str]:
	urls_to_keep = []
	include_t = tuple(include)
	exclude_t = tuple(exclude)
	if not include_t or "" in include_t:
		raise ValueError("include_prefixes is empty or contains an empty prefix.")
	if "" in exclude_t:
		raise ValueError("exclude_prefixes contains an empty prefix.")
	for url in sitemap:
		path = urlsplit(url).path.strip("/") + "/"
		if path.startswith(include_t) and not path.startswith(exclude_t):
			urls_to_keep.append(url)

	logging.info(f"{len(urls_to_keep)} url(s) was kept after filtering.")
	return urls_to_keep


def filter_urls(sitemap: list[str], keywords: list[str]) -> list[str]:
	urls_to_keep = []
	kw_set = set(kw.lower() for kw in keywords)
	if not kw_set or "" in kw_set:
		raise ValueError("keywords can't be empty")
	for url in sitemap:
		tokens = split_segments(url)
		if not kw_set.isdisjoint(tokens):
			urls_to_keep.append(url)

	logging.info(f"Found {len(urls_to_keep)} urls.")
	return list(urls_to_keep)
