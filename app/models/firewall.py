from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db import db


class Firewall(db.Model):
    __tablename__ = "firewalls"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(Text)

    policies = relationship(
        "FilteringPolicy", back_populates="firewall", cascade="all, delete-orphan"
    )
