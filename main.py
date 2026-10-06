import sys
import logging
from operator import itemgetter
from config.config import load_config, get_site_config
from crawler.crawler import (
	get_sitemap,
	group_by_branch,
	filter_urls,
	hit_ratio,
	select_urls,
)


def main():
	logging.basicConfig(level=logging.INFO)
	try:
		conf = load_config()
		site = get_site_config(conf, "vd")
	except ValueError as e:
		logging.error(e)
		sys.exit(1)

	sitemap = get_sitemap(url=site["base_url"])

	selected = select_urls(sitemap, site["include_prefixes"], site["exclude_prefixes"])
	print(selected)


if __name__ == "__main__":
	main()
