from typing import List

from sqlalchemy import Column, Integer, Double, func
from sqlalchemy.exc import SQLAlchemyError

from config.db.mysql.config import Base
from model.Clicks import Clicks


class Impressions(Base):
    __tablename__ = "impressions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    banner_id = Column(Integer)
    campaign_id = Column(Double)

    @staticmethod
    def get_top_banners_by_clicks(db, campaign_id: int, top_count: int) -> List[int]:
        try:
            query = db.query(Clicks.banner_id) \
                .outerjoin(Clicks, Clicks.banner_id == Impressions.banner_id) \
                .filter(Impressions.campaign_id == campaign_id) \
                .group_by(Impressions.banner_id) \
                .order_by(func.count(Clicks.click_id).desc()) \
                .limit(top_count)
            results = query.all()
            top_banners = [banner_id for banner_id, _ in results]
            return top_banners
        except SQLAlchemyError as e:
            # Handle exception
            print(f"An error occurred: {e}")
            return None
