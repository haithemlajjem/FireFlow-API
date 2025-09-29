from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RuleIn(BaseModel):
    action: str = Field(..., examples=["allow", "deny"])
    src: Optional[str] = None
    dst: Optional[str] = None
    protocol: Optional[str] = None

    @field_validator("action")
    def action_must_be_valid(cls, v):
        if v.lower() not in ("allow", "deny"):
            raise ValueError("action must be 'allow' or 'deny'")
        return v.lower()


class RuleOut(RuleIn):
    id: int

    model_config = {"from_attributes": True}


# Flasgger Swagger definitions
definitions = {
    "RuleIn": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["allow", "deny"],
                "example": "allow",
            },
            "src": {"type": "string", "example": "10.0.0.5"},
            "dst": {"type": "string", "example": "8.8.8.8"},
            "protocol": {"type": "string", "example": "tcp"},
        },
        "required": ["action"],
    },
    "RuleOut": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "example": 1},
            "action": {"type": "string", "example": "deny"},
            "src": {"type": "string", "example": "192.168.1.10"},
            "dst": {"type": "string", "example": "10.0.0.20"},
            "protocol": {"type": "string", "example": "udp"},
        },
    },
}
