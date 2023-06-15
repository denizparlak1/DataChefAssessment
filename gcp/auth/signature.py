from google.cloud import storage
from datetime import datetime, timedelta


def generate_signed_url(bucket_name, image_path, expiration=3600):
    """Generates a signed URL for accessing an image in Google Cloud Storage."""
    # Create a storage client
    client = storage.Client()

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Set the expiration time
    expiration_time = datetime.utcnow() + timedelta(seconds=expiration)

    # Generate the signed URL
    blob = bucket.blob(image_path)
    signed_url = blob.generate_signed_url(expiration=expiration_time)

    return signed_url
