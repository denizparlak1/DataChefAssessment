import os

from dotenv import load_dotenv

load_dotenv()

user = os.environ['user']
host = os.environ['host']
port = os.environ['port']
password = os.environ['password']
schema = os.environ['schema']
bucket = os.environ['bucket']

aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']
