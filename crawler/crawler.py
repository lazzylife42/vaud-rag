import json
import logging
from urllib.parse import urlsplit

from trafilatura import sitemaps


def get_sitemap(url):
	sitemap_path = "./crawler/sitemap.json"
	try:
		with open(sitemap_path, "r", encoding="utf-8") as f:
			sitemap = json.load(f)

	except FileNotFoundError:
		logging.warning(
			'File "sitemap.json" not found. '
			'Trying to parse it from BASE_URL.'
		)
		sitemap = sitemaps.sitemap_search(url=url)
		with open(sitemap_path, "w", encoding="utf-8") as f:
			json.dump(sitemap, f, indent=4)

	logging.info(f"Sitemap contains {len(sitemap)} urls.")
	return sitemap


def get_site_categories(sitemap):
	categories = set()
	for url in sitemap:
		path = urlsplit(url).path.strip("/")
		if path:
			categories.add(path.split("/")[0])

	logging.info(f"Found {len(categories)} categories.")
	return list(categories)


def filter_urls(sitemap, keywords):
	keywords = [kw.lower() for kw in keywords]
	urls_to_keep = []
	for url in sitemap:
		path = urlsplit(url).path.lower()
		if any(kw in path for kw in keywords):
			urls_to_keep.append(url)
			
	logging.info(f"Found {len(urls_to_keep)} urls.")
	return urls_to_keep
