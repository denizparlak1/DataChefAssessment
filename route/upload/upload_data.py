from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from config.db.mysql.config import get_db
from model.Clicks import Clicks
from model.Conversions import Conversions
from model.Images import Images
from model.Impressions import Impressions

router = APIRouter(prefix="/upload")


@router.post("/csv/api/")
async def upload_csv(file: UploadFile = File(...), table_name: str = Form(...), db: Session = Depends(get_db)):
    if file.filename.endswith('.csv'):
        # Process the CSV file
        contents = await file.read()
        data = pd.read_csv(BytesIO(contents))

        # Choose the processing logic based on the table_name
        if table_name == 'clicks':
            for index, row in data.iterrows():
                record = Clicks(click_id=row['click_id'], banner_id=row['banner_id'], campaign_id=row['campaign_id'],quarter_hour=row['quarter_hour'])
                db.add(record)
            db.commit()
        elif table_name == 'conversions':
            for index, row in data.iterrows():
                record = Conversions(conversation_id=row['conversation_id'], click_id=row['click_id'],revenue=row['revenue'],quarter_hour=row['quarter_hour'])
                db.add(record)
            db.commit()
        elif table_name == 'impressions':
            for index, row in data.iterrows():
                record = Impressions(banner_id=row['banner_id'], campaign_id=row['campaign_id'])
                db.add(record)
            db.commit()
        elif table_name == 'images':
            for index, row in data.iterrows():
                record = Images(url=row['url'])
                db.add(record)
            db.commit()
        else:
            raise HTTPException(status_code=400, detail="Invalid table name")

        return JSONResponse(content={"message": "File processed successfully"})
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
