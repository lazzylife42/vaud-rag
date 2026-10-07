import pytest

from crawler.robots import is_allowed, parse_robots, sitemaps_from_robots

UA = "vaud-rag/0.1 (contact: test@example.com)"


@pytest.mark.parametrize(
	"url, expected",
	[
		pytest.param("https://www.vd.ch/x?cHash=abc", False, id="cHash-refuse"),
		pytest.param("https://www.vd.ch/page?id=1", False, id="id-parameter-refuse"),
		pytest.param("https://www.vd.ch/page?L=0", False, id="language-L0-refuse"),
		pytest.param("https://www.vd.ch/page?L=1", True, id="language-L1-allow"),
		pytest.param(
			"https://www.vd.ch/fr/Configuration/x", False, id="configuration-dir-refuse"
		),
		pytest.param("https://www.vd.ch/typo3/x", False, id="typo3-dir-refuse"),
		pytest.param(
			"https://www.vd.ch/fileadmin/user_upload/accueil/Communique_presse/x.pdf",
			False,
			id="communique-presse-pdf-refuse",
		),
		pytest.param(
			"https://www.vd.ch/economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/demander-lindemnite-de-chomage",
			True,
			id="chomage-page-allow",
		),
		pytest.param(
			"https://www.vd.ch/?sitemap=1&cHash=abc",
			True,
			id="sitemap-with-cHash-allow",
		),
		pytest.param(
			"https://www.vd.ch/typo3temp/x.css", True, id="typo3temp-css-allow"
		),
		pytest.param(
			"https://www.vd.ch/typo3temp/x.html", False, id="typo3temp-html-refuse"
		),
	],
)
def test_is_allow(rp, url, expected):
	assert (
		is_allowed(
			rp=rp,
			url=url,
			user_agent=UA,
		)
		== expected
	)


@pytest.mark.parametrize(
	"empty_text",
	[
		pytest.param("", id="empty-string"),
		pytest.param("   \n", id="whitespace-string"),
	],
)
def test_parse_robots_empty(empty_text):
	with pytest.raises(ValueError, match="Can't parse an empty string"):
		parse_robots(robots_text=empty_text)


def test_sitmaps_from_robots(robots):
	assert sitemaps_from_robots(parse_robots(robots_text=robots)) == [
		"https://www.vd.ch/sitemap?type=1533906435"
	]
