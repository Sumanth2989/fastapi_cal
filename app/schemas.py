from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Literal

OperationType = Literal["add", "subtract", "multiply", "divide", "power"]

class CalcRequest(BaseModel):
    a: float = Field(..., description="Left operand")
    b: float = Field(..., description="Right operand")
    op: OperationType

    @field_validator("op")
    @classmethod
    def validate_op(cls, v: str) -> str:
        allowed = {"add", "subtract", "multiply", "divide", "power"}
        if v not in allowed:
            raise ValueError(f"Unsupported operation: {v}")
        return v

class CalcResponse(BaseModel):
    result: float
