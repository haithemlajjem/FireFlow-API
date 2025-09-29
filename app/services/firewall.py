"""
Service layer for Firewall operations.
Handles database logic for creating, retrieving, and deleting firewalls.
"""

import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.firewall import Firewall
from app.schemas.firewall import FirewallOut

logger = logging.getLogger(__name__)


def create_firewall(
    db: Session, name: str, description: str | None = None
) -> FirewallOut:
    """Create and persist a firewall."""
    logger.info(f"Creating firewall with name={name}")
    fw = Firewall(name=name, description=description)
    db.add(fw)
    try:
        db.commit()
        db.refresh(fw)
        logger.info(f"Firewall created with id={fw.id}")
    except IntegrityError:
        db.rollback()
        logger.error(f"Firewall creation failed: name '{name}' already exists")
        raise ValueError("Firewall with that name already exists")
    return FirewallOut.model_validate(fw)  # <- Pydantic v2 replacement


def update_firewall(
    db: Session, fw_id: int, name: str, description: str | None = None
) -> FirewallOut | None:
    """Update a firewall by ID."""
    fw = db.get(Firewall, fw_id)
    if not fw:
        logger.warning(f"Update failed: firewall not found id={fw_id}")
        return None

    logger.info(
        f"Updating firewall id={fw_id} with name={name} and description={description}"
    )
    fw.name = name
    fw.description = description
    try:
        db.commit()
        db.refresh(fw)
        logger.info(f"Firewall updated: id={fw.id}")
    except IntegrityError:
        db.rollback()
        logger.error(f"Firewall update failed: name '{name}' already exists")
        raise ValueError("Firewall with that name already exists")

    return FirewallOut.model_validate(fw)


def list_firewalls(db: Session) -> list[FirewallOut]:
    """List all firewalls."""
    fws = db.query(Firewall).all()
    logger.info(f"Listing {len(fws)} firewalls")
    return [FirewallOut.model_validate(fw) for fw in fws]


def get_firewall(db: Session, fw_id: int) -> FirewallOut | None:
    """Retrieve a firewall by ID."""
    fw = db.get(Firewall, fw_id)
    if fw:
        logger.info(f"Firewall retrieved: id={fw.id}")
        return FirewallOut.model_validate(fw)
    logger.warning(f"Firewall not found: id={fw_id}")
    return None


def delete_firewall(db: Session, fw_id: int) -> bool:
    """Delete a firewall by ID."""
    fw = db.get(Firewall, fw_id)
    if not fw:
        logger.warning(f"Delete failed: firewall not found id={fw_id}")
        return False
    db.delete(fw)
    db.commit()
    logger.info(f"Firewall deleted: id={fw_id}")
    return True
