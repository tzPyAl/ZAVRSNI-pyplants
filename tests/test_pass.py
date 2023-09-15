import pytest

@pytest.mark.parametrize("blink", ["mark", "tom", "travis"])
def test_pass(blink):
    print(blink)
    pass