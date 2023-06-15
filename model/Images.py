from sqlalchemy import Column, Integer, String

from config.config import Base, bucket
from gcp.auth.signature import generate_signed_url


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    url = Column(String(255))

    @classmethod
    def get_image_url(cls, banner_id,session):
        print(banner_id)
        """Returns the URL of an image based on the banner ID."""
        # Query the database to retrieve the image URL with the given banner ID
        image = session.query(cls.url).filter(cls.id == banner_id).first()
        # If the image URL exists, generate a signed URL for accessing it
        if image:
            signed_url = generate_signed_url(bucket, image.url)
            return signed_url

        # If the image URL does not exist or there is an error, return None
        return None