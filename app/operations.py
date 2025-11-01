from __future__ import annotations

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def power(a: float, b: float) -> float:
    # Simple exponent; Python handles negatives/floats naturally
    return a ** b
