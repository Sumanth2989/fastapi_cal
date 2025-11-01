import math
import pytest
from app import operations as ops

@pytest.mark.parametrize(
    "a,b,expected",
    [(1,2,3), (-1, 2, 1), (1.5, 2.5, 4.0)]
)
def test_add(a,b,expected):
    assert ops.add(a,b) == expected

@pytest.mark.parametrize(
    "a,b,expected",
    [(5,2,3), (-1, -2, 1), (2.5, 1.25, 1.25)]
)
def test_subtract(a,b,expected):
    assert ops.subtract(a,b) == expected

@pytest.mark.parametrize(
    "a,b,expected",
    [(3,2,6), (-3, 2, -6), (1.5, 2.0, 3.0)]
)
def test_multiply(a,b,expected):
    assert ops.multiply(a,b) == expected

def test_divide_normal():
    assert ops.divide(10,2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        ops.divide(1,0)

@pytest.mark.parametrize(
    "a,b,expected",
    [(2,3,8), (5,0,1), (9,0.5,3)]
)
def test_power(a,b,expected):
    assert ops.power(a,b) == pytest.approx(expected)
