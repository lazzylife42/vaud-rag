import pytest

from crawler.fetcher import compute_wait


class Test__compute_wait:
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
