import pytest

from crawler.robots import parse_robots


@pytest.fixture
def urls():
	return [
		"https://www.vd.ch/mobilite/automobile-et-navigation/navigation/controle-medical-lie-a-la-conduite-des-bateaux",
		"https://www.vd.ch/mobilite/automobile-et-navigation/navigation/retrait-de-permis",
		"https://www.vd.ch/mobilite/automobile-et-navigation/contacter-le-san",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/permis-de-conduire",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/permis-de-circulation-carte-grise-plaques-de-controle",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/permis-a-court-terme",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/plaques-dexportation",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/retrait-et-saisie-des-plaques",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/controles-techniques-expertises",
		"https://www.vd.ch/mobilite/automobile-et-navigation/frais-des-prestations-du-san/mesures-administratives-retrait-du-permis-de-conduire",
		"https://www.vd.ch/mobilite/loffre-de-mobilite-a-votre-disposition/transports-individuels-motorises-tim/rc-177-aclens-vufflens-la-ville-penthaz/actualite-rc-177",
		"https://www.vd.ch/etat-droit-finances/impots/impots-pour-les-individus/gerer-mes-acomptes",
		"https://www.vd.ch/infos-utiles/organiser-les-elections-communales-2026/titre-par-defaut",
		"https://www.vd.ch/etat-droit-finances/statistique/stat-exp/qui-sont-les-menages-qui-occupent-les-logements-nouvellement-construits-dans-le-canton",
		"https://www.vd.ch/etat-droit-finances/votations-et-elections/registre-cantonal-des-partis-politiques/union-democratique-du-centre-udc/udc-montreux-veytaux",
		"https://www.vd.ch/etat-droit-finances/egalite-entre-les-femmes-et-les-hommes/amoureux-se/respecter-le-consentement",
		"https://www.vd.ch/formation/orientation/telecharger-les-publications-de-loffice-cantonal-dorientation-scolaire-et-professionnelle/les-info-metiers-permettent-de-decouvrir-les-professions",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-bex",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-daclens",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-dagiez",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-dallaman",
		"https://www.vd.ch/etat-droit-finances/votations-et-elections/registre-cantonal-des-partis-politiques/les-vertes-mouvement-ecologiste/les-vertes-de-montreux",
		"https://www.vd.ch/environnement/biodiversite-et-paysage/grands-carnivores/protection-des-troupeaux",
		"https://www.vd.ch/monuments-sites/les-voies-historiques-protegees-en-bref",
		"https://www.vd.ch/monuments-sites/integrer-la-protection-du-patrimoine-dans-la-planification",
		"https://www.vd.ch/monuments-sites/comprendre-la-protection-des-biens-culturels-pbc",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-darnex-sur-nyon",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-darnex-sur-orbe",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-darzier-le-muids",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-dassens",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-daubonne",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-davenches",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-ballaigues",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-ballens",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-bassins",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-baulmes",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-bavois",
		"https://www.vd.ch/etat-droit-finances/votations-et-elections/registre-cantonal-des-partis-politiques/union-democratique-du-centre-udc/udc-b",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-begnins",
		"https://www.vd.ch/aides-financieres-et-soutien-social/aides-financieres-et-comment-les-demander/revenu-dinsertion-ri/bareme-des-loyers-pour-le-revenu-dinsertion-ri/bareme-a-loyer-pour-la-commune-de-belmont-sur-lausanne",
		"https://www.vd.ch/economie/prestations-destinees-aux-demandeuses-et-demandeurs-demploi/inscription-des-demandeurs-demploi-a-lorp",
		"https://www.vd.ch/territoire-et-construction/amenagement-du-territoire/projet-pilote-metamorphouse",
	]


@pytest.fixture
def keywords():
	return [
		"chomage",
		"orp",
		"lorp",
		"laci",
		"indemnite",
		"indemnites",
		"demandeur",
		"demandeurs",
		"demandeuse",
		"demandeuses",
		"demploi",
	]


@pytest.fixture
def robots():
	return """
User-agent: *
Allow: /
Disallow: /*/Configuration/*
Disallow: /*/Private/*
Disallow: /*&cHash=*
Disallow: /*?cHash=*
Disallow: /*&gclid=*
Disallow: /*?gclid=*
Disallow: /*&id=*
Disallow: /*?id=*
Disallow: /*&L=0*
Disallow: /*?L=0*
Disallow: /*&recherche=*
Disallow: /*?recherche=*
Disallow: /fileadmin/user_upload/_temp_/
Disallow: /fileadmin/user_upload/accueil/Communique_presse/*
Disallow: /fileadmin/_recycler_/
Disallow: /fileadmin/_temp_/
Disallow: /typo3/
Disallow: /typo3temp/
Allow: /*?sitemap=*&cHash=*
Allow: /typo3temp/*.ai
Allow: /typo3temp/*.bmp
Allow: /typo3temp/*.css
Allow: /typo3temp/*.css.*.gzip
Allow: /typo3temp/*.gif
Allow: /typo3temp/*.jpg
Allow: /typo3temp/*.jpeg
Allow: /typo3temp/*.js
Allow: /typo3temp/*.js.*.gzip
Allow: /typo3temp/*.pcx
Allow: /typo3temp/*.pdf
Allow: /typo3temp/*.png
Allow: /typo3temp/*.svg
Allow: /typo3temp/*.tga
Allow: /typo3temp/*.tif
Allow: /typo3temp/*.tiff
Sitemap: https://www.vd.ch/sitemap?type=1533906435
"""


@pytest.fixture
def rp(robots):
	return parse_robots(robots)
