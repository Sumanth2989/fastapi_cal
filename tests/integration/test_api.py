import pytest

def test_health_html(app_client):
    res = app_client.get("/")
    assert res.status_code == 200
    assert "<title>Calculator</title>" in res.text

@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"a": 1, "b": 2, "op": "add"}, 3),
        ({"a": 5, "b": 2, "op": "subtract"}, 3),
        ({"a": 3, "b": 4, "op": "multiply"}, 12),
        ({"a": 9, "b": 0.5, "op": "power"}, 3),
    ],
)
def test_calc_ok(app_client, payload, expected):
    res = app_client.post("/api/calc", json=payload)
    assert res.status_code == 200
    assert res.json()["result"] == pytest.approx(expected)

def test_calc_divide_by_zero(app_client):
    res = app_client.post("/api/calc", json={"a": 1, "b": 0, "op": "divide"})
    assert res.status_code == 400
    assert "Cannot divide by zero" in res.json()["detail"]

def test_calc_bad_op(app_client):
    res = app_client.post("/api/calc", json={"a": 1, "b": 2, "op": "mod"})
    assert res.status_code == 422  # pydantic validation
