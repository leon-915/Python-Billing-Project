"""Subscription related models and database functionality"""
from datetime import datetime
from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM
from src.models.plans import Plan
from src.models.base import db

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()

class SubscriptionStatus(Enum):
    """Enum representing possible subscription statuses"""
    new = "new"
    active = "active"
    suspended = "suspended"
    expired = "expired"

class Subscription(Base):
    """Model class to represent ATT subscriptions"""

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    phone_number =  Column(String(50))
    status = Column(ENUM(SubscriptionStatus), default=SubscriptionStatus.new)
    activation_date = Column(TIMESTAMP(timezone=True), nullable=True)
    expiry_date = Column(TIMESTAMP(timezone=True), nullable=True)

    plan_id = Column(Integer, ForeignKey('plans.id'))
    plan = relationship("Plan", back_populates="plans")
   

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.status}), "
            f"phone_number: {self.phone_number or '[no phone number]'}, ",
            f"plan: {self.plan_id}>"
        )

    @classmethod
    def get_subscriptions(cls, **kwargs):
        """Gets a list of Subscription objects using given kwargs

        Generates query filters from kwargs param using base class method

        Args:
            kwargs: key value pairs to apply as filters

        Returns:
            list: objects returned from query result

        """
        return cls.query.filter(**kwargs).all()



