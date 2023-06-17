import boto3
from datetime import datetime, timedelta
from config.enviroment.config import aws_access_key_id, aws_secret_access_key


class S3ClientSingleton:
    _instance = None

    def __new__(cls, aws_access_key_id, aws_secret_access_key):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.s3 = boto3.client('s3',
                                            aws_access_key_id=aws_access_key_id,
                                            aws_secret_access_key=aws_secret_access_key)
        return cls._instance


def generate_signed_urls(bucket_name, image_paths, expiration=3600):

    # Get or create the singleton S3 client
    s3_client = S3ClientSingleton(aws_access_key_id, aws_secret_access_key).s3

    # Create a list to store the signed URLs
    signed_urls = []

    # Generate signed URLs in batches
    for image_path in image_paths:
        # Set the expiration time
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration)

        # Generate the signed URL
        signed_url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': image_path
            },
            ExpiresIn=expiration
        )

        # Append the signed URL to the list
        signed_urls.append(signed_url)
    print(signed_urls)
    return signed_urls
