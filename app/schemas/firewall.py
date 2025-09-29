from typing import List, Optional

from pydantic import BaseModel

from app.schemas.policy import PolicyOut


class FirewallIn(BaseModel):
    name: str
    description: Optional[str] = None


class FirewallOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    policies: List[PolicyOut] = []

    model_config = {"from_attributes": True}


# Flasgger Swagger definitions
definitions = {
    "FirewallIn": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "example": "corp-fw"},
            "description": {"type": "string", "example": "Corporate edge firewall"},
        },
        "required": ["name"],
    },
    "FirewallOut": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "policies": {
                "type": "array",
                "items": {"$ref": "#/definitions/PolicyOut"},
            },
        },
    },
}
