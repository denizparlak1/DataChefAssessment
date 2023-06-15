from sqlalchemy import Column, Integer, Double, func, ForeignKey

from sqlalchemy.orm import relationship, joinedload, declarative_base

from config.config import Base
from model.Clicks import Clicks



class Conversions(Base):
    __tablename__ = "conversions"

    conversion_id = Column(Integer, primary_key=True)
    click_id = Column(Integer, ForeignKey('clicks.click_id'))
    revenue = Column(Double)

    clicks = relationship("Clicks", back_populates="conversions")

    @classmethod
    def get_banner_count_for_campaign(cls, session, campaign_id: int):
        try:
            banner_count = session.query(func.count(Clicks.banner_id.distinct())). \
                join(cls, Clicks.click_id == cls.click_id). \
                filter(Clicks.campaign_id == campaign_id). \
                scalar()

            return banner_count

        except Exception as e:
            # Handle the exception
            print(f"An error occurred: {e}")
            return None

    @classmethod
    def get_top_banners_by_revenue(cls, session, campaign_id: int, limit: int = 10):
        try:
            # Building the query
            banners = session.query(
                Clicks.banner_id,
                func.sum(Conversions.revenue).label('total_revenue')
            ).join(
                Clicks, Conversions.click_id == Clicks.click_id
            ).filter(
                Clicks.campaign_id == campaign_id
            ).group_by(
                Clicks.banner_id
            ).order_by(
                func.sum(Conversions.revenue).desc()
            ).limit(limit).all()
            # Extract the banner_id from the result
            banner_ids = [banner[0] for banner in banners]

            return banner_ids

        except Exception as e:
            # Handle the exception
            print(f"An error occurred: {e}")
            return None

