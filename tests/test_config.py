from src.config import CHECK_INTERVAL


def test_check_interval_is_positive():
    assert CHECK_INTERVAL > 0
