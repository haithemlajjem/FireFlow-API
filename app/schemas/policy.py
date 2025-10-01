from typing import List, Optional

from pydantic import BaseModel

from app.schemas.rule import RuleIn, RuleOut


class PolicyIn(BaseModel):
    name: str
    rules: Optional[List[RuleIn]] = []


class PolicyOut(BaseModel):
    id: int
    name: str
    rules: List[RuleOut] = []

    model_config = {"from_attributes": True}


# Flasgger Swagger definitions
definitions = {
    "PolicyIn": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "example": "default-policy"},
            "rules": {
                "type": "array",
                "items": {"$ref": "#/definitions/RuleIn"},
                "example": [
                    {
                        "action": "allow",
                        "src": "10.0.0.0/24",
                        "dst": "0.0.0.0/0",
                        "protocol": "tcp",
                    }
                ],
            },
        },
        "required": ["name"],
    },
    "PolicyOut": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "example": 1},
            "name": {"type": "string", "example": "default-policy"},
            "rules": {
                "type": "array",
                "items": {"$ref": "#/definitions/RuleOut"},
            },
        },
    },
}
