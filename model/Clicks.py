from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from config.db.mysql.config import Base


class Clicks(Base):
    __tablename__ = "clicks"

    click_id = Column(Integer, primary_key=True)
    banner_id = Column(Integer)
    campaign_id = Column(Integer)
    quarter_hour = Column(Integer)

    conversions = relationship("Conversions", back_populates="clicks")
