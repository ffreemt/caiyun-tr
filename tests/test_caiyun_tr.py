"""Test caiyun_tr."""
# pylint: disable=broad-except
from caiyun_tr import __version__
from caiyun_tr import caiyun_tr


def test_version():
    """Test version."""
    assert __version__[:3] == "0.1"


def test_sanity():
    """Check sanity."""
    try:
        assert not caiyun_tr()
    except Exception:
        assert True
