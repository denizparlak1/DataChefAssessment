from typing import List, Union
from sqlalchemy import Column, Integer, Double, func, ForeignKey
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from config.db.mysql.config import Base
from model.Clicks import Clicks
import random

class Conversions(Base):
    __tablename__ = "conversions"

    conversion_id = Column(Integer, primary_key=True)
    click_id = Column(Integer, ForeignKey('clicks.click_id'))
    revenue = Column(Double)
    quarter_hour = Column(Integer)

    clicks = relationship("Clicks", back_populates="conversions")

    @classmethod
    def get_banner_count_for_campaign(cls, session, campaign_id: int, quarter_hour: int):
        try:
            banner_count = (
                session.query(func.count(Clicks.banner_id.distinct()))
                .join(cls, cls.click_id == Clicks.click_id)
                .filter(Clicks.campaign_id == campaign_id)
                .filter(cls.quarter_hour == quarter_hour)
                .scalar()
            )
            return banner_count

        except SQLAlchemyError as e:
            # Handle the exception
            print(f"An error occurred: {e}")
            return None

    @classmethod
    def get_top_banners_by_revenue(cls, session, campaign_id: int, quarter: int,limit: int = 10, exclude_banner_ids: Union[List[int], None] = None):
        try:
            # Building the base query
            query = session.query(
                Clicks.banner_id,
                func.sum(Conversions.revenue).label('total_revenue')
            ).join(
                Clicks, Conversions.click_id == Clicks.click_id
            ).filter(
                and_(
                    Clicks.campaign_id == campaign_id,
                    Conversions.quarter_hour == quarter,
                    Clicks.quarter_hour == quarter
                )
            ).group_by(
                Clicks.banner_id
            ).order_by(
                func.sum(Conversions.revenue).desc()
            )

            # Adding the notin_ filter if exclude_banner_ids is provided and not empty

            if exclude_banner_ids is not None and len(exclude_banner_ids) > 0:
                query = query.filter(Clicks.banner_id.notin_(exclude_banner_ids))
            # Adding the limit
            query = query.limit(limit)

            # Executing the query
            banners = query.all()

            # Extracting the banner_id from the result
            banner_ids = [banner[0] for banner in banners]

            # Shuffling the banner IDs to create a random sequence
            random.shuffle(banner_ids)

            return banner_ids

        except Exception as e:
            # Handling the exception
            print(f"An error occurred: {e}")
            return None

    @classmethod
    def banner_combined_query(cls, session, campaign_id: int, X: int = 5, quarter_hour: int = 1):
        try:
            revenue_banners = (
                session.query(
                    Clicks.banner_id,
                    func.sum(cls.revenue).label('total_revenue')
                )
                .join(cls, cls.click_id == Clicks.click_id)
                .filter(Clicks.campaign_id == campaign_id)
                .filter(cls.quarter_hour == quarter_hour)  # Add dynamic WHERE statement for quarter_hour column
                .group_by(Clicks.banner_id)
                .order_by(func.sum(cls.revenue).desc())
                .limit(X)
                .subquery()
            )

            clicks_banners = (
                session.query(
                    Clicks.banner_id,
                    func.count().label('total_clicks')
                )
                .filter(Clicks.campaign_id == campaign_id)
                .filter(Clicks.quarter_hour == quarter_hour)  # Add dynamic WHERE statement for quarter_hour column
                .group_by(Clicks.banner_id)
                .order_by(func.count().desc())
                .limit(5 - X)
                .subquery()
            )

            combined_result = (
                session.query(revenue_banners.c.banner_id)
                .union(
                    session.query(clicks_banners.c.banner_id)
                )
                .all()
            )
            combined_result = revenue_banners + clicks_banners
            random.shuffle(combined_result)

            return [result[0] for result in combined_result]

        except SQLAlchemyError as e:
            # Handle the exception
            print(f"An error occurred: {e}")
            return None
