"""
Service layer for Firewall Rule operations.
"""

import logging

from sqlalchemy.orm import Session

from app.models.policy import FilteringPolicy
from app.models.rule import Rule
from app.schemas.rule import RuleOut

logger = logging.getLogger(__name__)


def add_rule(
    db: Session,
    policy_id: int,
    action: str,
    src: str | None = None,
    dst: str | None = None,
    protocol: str | None = None,
) -> RuleOut:
    """Add a new rule to a policy."""
    logger.info(f"Adding rule to policy id={policy_id}, action={action}")
    p = db.get(FilteringPolicy, policy_id)
    if not p:
        logger.error(f"Policy not found: id={policy_id}")
        raise ValueError("Policy not found")

    r = Rule(action=action, src=src, dst=dst, protocol=protocol, policy=p)
    db.add(r)
    db.commit()
    db.refresh(r)
    logger.info(f"Rule created with id={r.id} for policy id={policy_id}")
    return RuleOut.model_validate(r)  # <- Pydantic v2


def list_rules(db: Session, policy_id: int) -> list[RuleOut]:
    """List all rules for a policy."""
    p = db.get(FilteringPolicy, policy_id)
    if not p:
        logger.error(f"Policy not found for listing rules: id={policy_id}")
        raise ValueError("Policy not found")
    logger.info(f"Listing {len(p.rules)} rules for policy id={policy_id}")
    return [RuleOut.model_validate(r) for r in p.rules]


def delete_rule(db: Session, rule_id: int) -> bool:
    """Delete a rule by ID."""
    r = db.get(Rule, rule_id)
    if not r:
        logger.warning(f"Delete failed: rule not found id={rule_id}")
        return False
    db.delete(r)
    db.commit()
    logger.info(f"Rule deleted: id={rule_id}")
    return True
