from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import db


class FilteringPolicy(db.Model):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    firewall_id = Column(Integer, ForeignKey("firewalls.id", ondelete="CASCADE"))

    firewall = relationship("Firewall", back_populates="policies")
    rules = relationship("Rule", back_populates="policy", cascade="all, delete-orphan")
