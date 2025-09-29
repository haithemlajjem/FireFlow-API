"""
Service layer for Filtering Policy operations.
Handles database logic for creating, listing, and deleting policies.
"""

import logging

from sqlalchemy.orm import Session

from app.models.firewall import Firewall
from app.models.policy import FilteringPolicy
from app.models.rule import Rule
from app.schemas.policy import PolicyOut

logger = logging.getLogger(__name__)


def add_policy(db: Session, fw_id: int, name: str, rules: list[dict]) -> PolicyOut:
    """Attach a new policy to a firewall with optional rules."""
    logger.info(f"Adding policy '{name}' to firewall id={fw_id}")
    fw = db.get(Firewall, fw_id)
    if not fw:
        logger.error(f"Firewall not found: id={fw_id}")
        raise ValueError("Firewall not found")

    policy = FilteringPolicy(name=name, firewall=fw)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    logger.info(f"Policy created with id={policy.id}")

    for r in rules or []:
        rule = Rule(
            action=r["action"],
            src=r.get("src"),
            dst=r.get("dst"),
            protocol=r.get("protocol"),
            policy=policy,
        )
        db.add(rule)
    db.commit()
    db.refresh(policy)
    logger.info(f"Added {len(rules or [])} rules to policy id={policy.id}")

    return PolicyOut.model_validate(policy)  # <- Pydantic v2


def list_policies(db: Session, fw_id: int) -> list[PolicyOut]:
    """List all policies belonging to a firewall."""
    fw = db.get(Firewall, fw_id)
    if not fw:
        logger.error(f"Firewall not found for listing policies: id={fw_id}")
        raise ValueError("Firewall not found")
    policies = fw.policies
    logger.info(f"Listing {len(policies)} policies for firewall id={fw_id}")
    return [PolicyOut.model_validate(p) for p in policies]


def delete_policy(db: Session, policy_id: int) -> bool:
    """Delete a policy by ID."""
    p = db.get(FilteringPolicy, policy_id)
    if not p:
        logger.warning(f"Delete failed: policy not found id={policy_id}")
        return False
    db.delete(p)
    db.commit()
    logger.info(f"Policy deleted: id={policy_id}")
    return True
