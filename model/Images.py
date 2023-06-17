from sqlalchemy import Column, Integer, String

from aws.s3.signature import generate_signed_urls
from config.db.mysql.config import Base
from config.enviroment.config import bucket
#from gcp.auth.signature import generate_signed_urls


class Images(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    url = Column(String(255))

    @classmethod
    def get_image_urls(cls, banner_ids: list, session):
        """Returns the URLs of images based on the banner IDs."""
        # Query the database to retrieve the image URLs with the given banner IDs
        images = session.query(cls.id, cls.url).filter(cls.id.in_(banner_ids)).all()

        # Get the list of image URLs
        image_paths = [image.url for image in images]

        # Generate the signed URLs in batches
        #signed_urls = generate_signed_urls(bucket, image_paths)
        signed_urls = generate_signed_urls(bucket, image_paths)
        # Create a dictionary to store the image URLs by ID
        image_urls = {image.id: signed_urls[index] for index, image in enumerate(images)}

        return image_urls
