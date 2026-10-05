import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"

REQUIRED = {
	"base_url": str,
	"languages": list,
	"delay_seconds": (int, float),
	"min_text_chars": int,
	"include_prefixes": list,
	"exclude_prefixes": list,
	"explore_keywords": list,
}

def load_config(path=CONFIG_PATH):
	try:
		with open(path, "r", encoding="utf-8") as f:
			return yaml.safe_load(f)
	except FileNotFoundError as e:
		raise ValueError(f"Config not found: {path}.") from e

def validate_site(site):
	name = site.get("name", "?")
	for key, expected in REQUIRED.items():
		if key not in site:
			raise ValueError(f"site '{name}': '{key}' is missing")
		value = site[key]
		if isinstance(value, bool) or not isinstance(value, expected):
			names = expected if isinstance(expected, tuple) else (expected,)
			expected_names = "|".join(t.__name__ for t in names)
			raise ValueError(
				f"site '{name}': '{key}' must be {expected_names}, "
				f"got {type(value).__name__}"
			)
	if site["delay_seconds"] < 1:
		raise ValueError(
			f"site '{name}': 'delay_seconds' must be >= 1, "
			f"got {site['delay_seconds']}."
		)

	return site

def get_site_config(conf, site_name):
	if not isinstance(conf, dict):
		raise ValueError("Config is empty or not a mapping")

	crawler = conf.get("crawler")
	if not isinstance(crawler, dict):
		raise ValueError("'crawler' is missing or not a mapping")

	sites = crawler.get("sites")
	if not isinstance(sites, list):
		raise ValueError("'crawler.sites' is missing or not a list")

	for site in sites:
		if not isinstance(site, dict) or "name" not in site:
			raise ValueError("Each site must be a mapping with a 'name'")
		if site["name"] == site_name:
			return validate_site(site)

	raise ValueError(f"Site '{site_name}' not found")
