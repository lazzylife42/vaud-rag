from collections import Counter

import pytest

from crawler.crawler import (
	filter_urls,
	group_by_branch,
	hit_ratio,
	select_urls,
	split_segments,
)


class TestGroupByBranch:
	def test_no_depth(self, urls):
		with pytest.raises(ValueError, match="depth must be >= 1"):
			group_by_branch(urls=urls, depth=0)

	def test_no_urls(self):
		assert group_by_branch(urls=[], depth=3) == Counter()

	def test_depth_2(self, urls):
		counter = group_by_branch(urls=urls, depth=2)
		assert sum(counter.values()) == len(urls)
		assert counter["monuments-sites/les-voies-historiques-protegees-en-bref/"] == 1
		assert counter["mobilite/automobile-et-navigation/"] == 10

	def test_root_path(self):
		assert group_by_branch(["https://www.vd.ch/"], depth=2) == Counter()


@pytest.mark.parametrize(
	"url, expected",
	[
		(
			"https://www.vd.ch/economie/demander-lindemnite-de-chomage",
			["economie", "demander", "lindemnite", "de", "chomage"],
		),
		("https://www.vd.ch/", []),
		("https://www.vd.ch/a--b", ["a", "b"]),
		("https://www.vd.ch/A/B-C", ["a", "b", "c"]),
	],
)
def test_split_segments(url, expected):
	assert split_segments(url) == expected


class TestFilterUrls:
	def test_does_not_match_substring(self):
		sitemap = [
			"https://www.vd.ch/economie/inscription-des-demandeurs-demploi-a-lorp",
			"https://www.vd.ch/economie/corporation-x",
		]
		filtered = filter_urls(sitemap=sitemap, keywords=["orp", "lorp"])
		assert filtered == [
			"https://www.vd.ch/economie/inscription-des-demandeurs-demploi-a-lorp"
		]

	def test_matches_keyword_case_insensitive(self):
		url = "https://www.vd.ch/economie/inscription-des-demandeurs-demploi-a-l-orp"
		filtered = filter_urls(sitemap=[url], keywords=["ORP"])
		assert filtered == [url]

	def test_keeps_sitemap_order(self):
		sitemap = [
			"https://www.vd.ch/a",
			"https://www.vd.ch/b",
			"https://www.vd.ch/c",
			"https://www.vd.ch/d",
		]
		filtered = filter_urls(sitemap=sitemap, keywords=["a", "b", "d"])
		assert filtered == [sitemap[0], sitemap[1], sitemap[3]]

	def test_empty_keywords_raises(self, urls):
		with pytest.raises(ValueError, match="keywords can't be empty"):
			filter_urls(sitemap=urls, keywords=[])

	def test_empty_string_keyword_raises(self, urls):
		with pytest.raises(ValueError, match="keywords can't be empty"):
			filter_urls(sitemap=urls, keywords=[""])

	def test_no_match_returns_empty_list(self):
		filtered = filter_urls(
			sitemap=["https://www.vd.ch/economie/autre-chose"], keywords=["orp", "lorp"]
		)
		assert filtered == []


class TestSelectUrls:
	@pytest.mark.parametrize(
		"include, exclude, message",
		[
			([], ["a/"], "include_prefixes"),
			([""], ["a/"], "include_prefixes"),
			(["a/"], [""], "exclude_prefixes"),
		],
	)
	def test_raises(self, urls, include, exclude, message):
		with pytest.raises(ValueError, match=message):
			select_urls(sitemap=urls, include=include, exclude=exclude)

	def test_nominal(self):
		sitemap = [
			"https://www.vd.ch/economie/a",
			"https://www.vd.ch/economie/publications/b",
			"https://www.vd.ch/finance/c",
		]
		selected = select_urls(
			sitemap=sitemap, include=["economie/"], exclude=["economie/publications/"]
		)
		assert selected == [sitemap[0]]

	def test_trailing_slash_trap(self):
		selected = select_urls(
			sitemap=["https://www.vd.ch/a/publications"],
			include=["a/"],
			exclude=["a/publications/"],
		)
		assert selected == []

	def test_empty_exclude_ok(self):
		sitemap = [
			"https://www.vd.ch/economie/a",
			"https://www.vd.ch/economie/b",
			"https://www.vd.ch/economie/c",
		]
		selected = select_urls(sitemap=sitemap, include=["economie/"], exclude=[])
		assert selected == sitemap

	def test_keeps_sitemap_order(self):
		sitemap = [
			"https://www.vd.ch/economie/c",
			"https://www.vd.ch/economie/a",
			"https://www.vd.ch/economie/b",
		]
		selected = select_urls(sitemap=sitemap, include=["economie/"], exclude=[])
		assert selected == sitemap

	def test_no_match_returns_empty_list(self):
		sitemap = [
			"https://www.vd.ch/economie/a",
			"https://www.vd.ch/economie/b",
			"https://www.vd.ch/economie/c",
		]
		selected = select_urls(sitemap=sitemap, include=["orp/"], exclude=[])
		assert selected == []


class TestHitRatio:
	def test_ratio(self):
		rows = hit_ratio(
			total=Counter({"a/": 10, "c/": 100}),
			hits=Counter({"a/": 5, "c/": 2}),
		)
		assert [row[0] for row in rows] == ["a/", "c/"]
		assert rows[0][1:3] == (5, 10)
		assert rows[0][3] == pytest.approx(0.5)
		assert rows[1][1:3] == (2, 100)
		assert rows[1][3] == pytest.approx(0.02)

	def test_missing_total_raises(self):
		with pytest.raises(ValueError, match="total key can't be zero"):
			hit_ratio(total=Counter(), hits=Counter({"a/": 5, "c/": 2}))

	def test_empty_hits(self):
		count = hit_ratio(total=Counter({"a/": 10, "c/": 100}), hits=Counter())
		assert count == []

	def test_sorted_descending(self):
		count = hit_ratio(
			total=Counter({"a/": 10, "b/": 5, "c/": 100}),
			hits=Counter({"a/": 5, "b/": 2, "c/": 2}),
		)
		assert [row[0] for row in count] == ["a/", "b/", "c/"]
