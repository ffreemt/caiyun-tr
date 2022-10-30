"""Test unsupported pair."""
import pytest
from caiyun_tr import caiyun_tr

def test_unsupported_pair_x():
    """Test to_lang="x"."""
    # with pytest.raises(RuntimeError) as excinfo:
    # assert "unsupport" in str(excinfo.value)

    with pytest.raises(Exception, match=r".*(NOT IMPLEMENTED|Unsupported).*") as excinfo:
        caiyun_tr("test", to_lang="x")
        
    with pytest.raises(Exception, match=r".*(NOT IMPLEMENTED|Unsupported).*") as excinfo:
        caiyun_tr("test", to_lang="rux")