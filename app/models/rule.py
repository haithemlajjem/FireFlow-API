from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import db


class Rule(db.Model):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    action = Column(String(16), nullable=False)  # 'allow' or 'deny'
    src = Column(String(64), nullable=True)
    dst = Column(String(64), nullable=True)
    protocol = Column(String(16), nullable=True)
    policy_id = Column(Integer, ForeignKey("policies.id", ondelete="CASCADE"))

    policy = relationship("FilteringPolicy", back_populates="rules")
