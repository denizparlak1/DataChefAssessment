from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, joinedload, declarative_base

from config.config import Base


class Clicks(Base):
    __tablename__ = "clicks"

    click_id = Column(Integer, primary_key=True)
    banner_id = Column(Integer)
    campaign_id = Column(Integer)

    conversions = relationship("Conversions", back_populates="clicks")

