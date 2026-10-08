import pytest
from protego import Protego

from crawler.fetcher import RobotsDisallowed, check_allowed, compute_wait


class TestCheckAllowed:
	@pytest.fixture
	def setup_data(self):
		robots_txt_content = "User-agent: *\nDisallow: /typo3/"
		rp = Protego.parse(robots_txt_content)
		allowed_host = "www.vd.ch"
		user_agent = "vaud-rag/0.1"
		return rp, allowed_host, user_agent

	def test_allowed_url_returns_none(self, setup_data):
		rp, allowed_host, user_agent = setup_data
		result = check_allowed(
			rp, "https://www.vd.ch/chomage", user_agent, allowed_host
		)
		assert result is None

	def test_other_host_raises(self, setup_data):
		rp, allowed_host, user_agent = setup_data
		with pytest.raises(RobotsDisallowed, match="not from the same host"):
			check_allowed(rp, "https://autre.com/chomage", user_agent, allowed_host)

	def test_host_comparison_ignores_case_and_port(self, setup_data):
		rp, allowed_host, user_agent = setup_data
		result = check_allowed(
			rp, "https://WWW.VD.CH:443/chomage", user_agent, allowed_host
		)
		assert result is None

	def test_subdomain_is_other_host(self, setup_data):
		rp, allowed_host, user_agent = setup_data
		with pytest.raises(RobotsDisallowed, match="not from the same host"):
			check_allowed(rp, "https://vd.ch/chomage", user_agent, allowed_host)

		with pytest.raises(RobotsDisallowed, match="not from the same host"):
			check_allowed(rp, "https://www.vd.ch.evil.com/x", user_agent, allowed_host)

	def test_disallowed_path_raises(self, setup_data):
		rp, allowed_host, user_agent = setup_data
		with pytest.raises(RobotsDisallowed, match="forbidden in the robots.txt"):
			check_allowed(rp, "https://www.vd.ch/typo3/x", user_agent, allowed_host)

	def test_url_without_hostname_raises_value_error(self, setup_data):
		rp, allowed_host, user_agent = setup_data
		with pytest.raises(ValueError, match="doesn't have a hostname"):
			check_allowed(rp, "/chomage", user_agent, allowed_host)


class TestComputeWait:
	def test_compute_wait_first_request_returns_zero(self):
		timer = compute_wait(None, 10.0, 2.0)
		assert timer == pytest.approx(0.0)

	def test_compute_wait_returns_remaining_delay(self):
		timer = compute_wait(10.0, 10.5, 2.0)
		assert timer == pytest.approx(1.5)

	def test_compute_wait_returns_zero_when_delay_elapsed(self):
		timer = compute_wait(10.0, 13.0, 2.0)
		assert timer == pytest.approx(0.0)

	def test_compute_wait_rejects_negative_delay(self):
		with pytest.raises(ValueError, match="delay param can't be negative"):
			compute_wait(10.0, 13.0, -1.0)

	def test_compute_wait_same_instant_returns_full_delay(self):
		timer = compute_wait(10.0, 10.0, 2.0)
		assert timer == pytest.approx(2.0)

	def test_compute_wait_last_request_zero_is_not_first_request(self):
		timer = compute_wait(0.0, 1.0, 2.0)
		assert timer == pytest.approx(1.0)
