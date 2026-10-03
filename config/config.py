import logging
import yaml


def load_config():
	try:
		with open("./config/config.yaml", "r", encoding="utf-8") as f:
			return yaml.safe_load(f)
	except FileNotFoundError as e:
		logging.error(f"Something went wrong\n{e}")
		raise SystemExit(1)


def get_site_config(conf, site_name):
	for site in conf["crawler"]["sites"]:
		if site["name"] == site_name:
			return site

	raise ValueError(f"Site '{site_name}' not found")
