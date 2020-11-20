"""Cycle related models and database functionality"""
from src.models.base import db



from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BillingCycle(Base):
    """Model class to represent billing cycle dates

    NOTE: this is probably temporary....
    """

    __tablename__ = "billing_cycles"

    id = Column(Integer, primary_key=True)
    start_date = Column(TIMESTAMP(timezone=True))
    end_date = Column(TIMESTAMP(timezone=True))

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id}, "
            f"start_date: {self.start_date}, end_date: {self.end_date}>"
        )

    @classmethod
    def get_current_cycle(cls, date=None):
        """Helper method to get current billing cycle of given date

        Args:
            date (date): date to get billing cycle for

        Returns:
            object: billing cycle object, if any

        """
        if not date:
            date = datetime.now()
        return cls.query.filter(
            cls.start_date <= date, cls.end_date > date).first()
