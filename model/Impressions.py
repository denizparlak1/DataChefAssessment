from sqlalchemy import Column, Integer, Double

from sqlalchemy.orm import relationship, joinedload, declarative_base

from config.config import Base


class Impressions(Base):
    __tablename__ = "impressions"

    id = Column(Integer, primary_key=True,autoincrement=True)
    banner_id = Column(Integer)
    campaign_id = Column(Double)
