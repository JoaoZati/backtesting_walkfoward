import pytest


@pytest.mark.parametrize(
    'a',
    [1, 2],
)
def test_simple(a):
    assert isinstance(a, int)
