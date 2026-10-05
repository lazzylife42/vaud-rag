import logging
import sys
from config.config import load_config, get_site_config
from crawler.crawler import get_sitemap, filter_urls

def main():
	logging.basicConfig(level=logging.INFO)
	try:
		conf = load_config()
		site = get_site_config(conf, "vd")
	except ValueError as e:
		logging.error(e)
		sys.exit(1)

	sitemap = get_sitemap(
		url=site["base_url"]
	)

	matching = filter_urls(
		sitemap=sitemap,
		keywords=site["explore_keywords"]
	)

	print(matching)


if __name__ == "__main__":
	main()
