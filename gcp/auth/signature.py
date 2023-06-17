from google.cloud import storage
from google.oauth2 import service_account
from datetime import datetime, timedelta


def generate_signed_urls(bucket_name, image_paths, expiration=3600):
    # Path to your service account JSON key file
    key_path = "/Users/denizparlak/Desktop/pc-api-4750275236482751782-669-370491900600.json"

    # Create credentials from the service account JSON key file
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # Create a storage client using the credentials
    client = storage.Client(credentials=credentials)

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Create a list to store the signed URLs
    signed_urls = []

    # Generate signed URLs in batches
    for image_path in image_paths:
        # Get the blob (object) within the bucket
        blob = bucket.blob(image_path)

        # Set the expiration time
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration)

        # Generate the signed URL
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=expiration_time,
            method="GET"
        )

        # Append the signed URL to the list
        signed_urls.append(signed_url)

    return signed_urls
