import pytest
from collections import Counter
from crawler.crawler import (
	group_by_branch,
	hit_ratio,
	split_segments,
	select_urls,
	filter_urls,
)


class Test__group_by_branch:
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
