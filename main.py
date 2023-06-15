from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config.config import Database
from model.Conversions import Conversions
from model.Images import Images

# Set up FastAPI app
app = FastAPI()


# Dependency to get database session
def get_db():
    db = Database.get_instance().Session()
    try:
        yield db
    finally:
        db.close()



@app.get("/campaigns/{campaign_id}")
async def get_banner_count(campaign_id: int, db: Session = Depends(get_db)):
    banner_count = Conversions.get_banner_count_for_campaign(db, campaign_id)
    if banner_count >= 10:
       top_banners = Conversions.get_top_banners_by_revenue(db, campaign_id)

    elif banner_count >= 5 and banner_count < 10:
        top_banners = Conversions.get_top_banners_by_revenue(db, campaign_id, limit=banner_count)

    # Construct the response data
    response_data = [
        {"banner_id": banner_id, "signed_url": Images.get_image_url(banner_id,db)}
        for banner_id in top_banners
    ]

    return response_data




