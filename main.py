import logging
import os
import sys

from dotenv import load_dotenv

from config.config import get_site_config, load_config
from crawler.crawler import get_sitemap, select_urls

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
	mail = os.environ.get("MAIL")
	if not mail:
		raise ValueError("MAIL not found in env.")
	UA = f"vaud-rag/0.1 (contact: {mail})"
	print(UA)
	try:
		conf = load_config()
		site = get_site_config(conf, "vd")
	except ValueError as e:
		logger.error(e)
		sys.exit(1)

	sitemap = get_sitemap(url=site["base_url"])

	selected = select_urls(sitemap, site["include_prefixes"], site["exclude_prefixes"])
	print(selected)


if __name__ == "__main__":
	main()
