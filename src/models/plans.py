"""Plans and Service related models and database functionality"""
from src.models.base import db
from sqlalchemy import Table, Column, Integer, ForeignKey, String, BigInteger, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
import psycopg2

DATABASE_URI = 'postgres+psycopg2://postgres:123456@localhost:5432/wingattbilling'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()
Base = declarative_base()


class Plan(Base):
    """Model class to represent mobile service plans"""
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    # amount of data available for a given billing cycle
    
    mb_available = Column(BigInteger)
    is_unlimited = Column(Boolean)

    subscription = relationship("Subscription", back_populates="plans")
    att_plan_version = relationship("ATTPlanVersion", back_populates="plans")

    # subscription = relationship("Subscribe", back_populates="plans")
    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.id} ({self.description})>"
        )
    def getmb():

        return ("1024")

        
class ATTPlanVersion(Base):
    """Model class to represent ATT plan version

    Custom versioning class to keep track of plans enabled ATT side
    """
    __tablename__ = "att_plan_versions"
    id = Column(Integer, primary_key=True)
    subscription_id = Column(
        Integer, ForeignKey("subscriptions.id"), nullable=False
    )
    subscription = relationship("Subscription", back_populates="subscriptions")
    
    plan_id = Column(String(30), ForeignKey("plans.id"), nullable=False)
    plan = relationship("Plan", back_populates="plans")

    start_effective_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_effective_date = Column(TIMESTAMP(timezone=True), nullable=False)

    mb_available = Column(BigInteger)

    def __repr__(self):  # pragma: no cover
        return (
            f"<{self.__class__.__name__}: {self.subscription_id}, "
            f"{str(self.plan_id)} ({self.start_effective_date} - "
            f"{self.end_effective_date}) "
        )
    def getmb(id):
        # r = s.query(Plan).filter(Plan.id== self.plan_id).first().get('mb_available')
        # return (r.mb_available)

        connection = psycopg2.connect(user="postgres",
                                  password="123456",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="wingattbilling")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select mb_available from plans where id=" + id
        cursor.execute(postgreSQL_select_Query)
        mobile_records_one = cursor.fetchone()
        print(mobile_records_one)
        print("r")
        return(1048)









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






