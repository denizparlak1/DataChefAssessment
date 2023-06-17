from sqlalchemy import Column, Integer, Double

from config.db.mysql.config import Base


class Impressions(Base):
    __tablename__ = "impressions"

    id = Column(Integer, primary_key=True,autoincrement=True)
    banner_id = Column(Integer)
    campaign_id = Column(Double)
