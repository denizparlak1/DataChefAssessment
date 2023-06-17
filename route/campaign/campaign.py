import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.db.mysql.config import Database, get_db
from model.Conversions import Conversions
from model.Images import Images
from utils.cookie.helper import get_unique_id, update_banner_ids
from utils.utils import get_quarter

router = APIRouter(prefix="/campaigns")


@router.get("/{campaign_id}/")
async def get_banner_count(request: Request, campaign_id: int, db: Session = Depends(get_db)):
    quarter = await get_quarter()

    unique_id, exclude_banner_ids = get_unique_id(request.cookies.get("unique_id"))

    banner_count = Conversions.get_banner_count_for_campaign(db, campaign_id, quarter.value)
    if banner_count >= 10:
        top_banners = Conversions.get_top_banners_by_revenue(db, campaign_id, quarter.value, 10, exclude_banner_ids)
    elif 5 <= banner_count < 10:
        top_banners = Conversions.get_top_banners_by_revenue(db, campaign_id, limit=banner_count)
    elif 1 <= banner_count < 5:
        top_banners = Conversions.banner_combined_query(db, campaign_id, limit=banner_count)

    image_urls = Images.get_image_urls(top_banners, db)

    update_banner_ids(unique_id, top_banners)

    return image_urls
