from backend.storage.s3 import S3Storage
from config import settings


class PastesStorage(S3Storage):
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    region_name = settings.AWS_REGION
    endpoint_url = "https://s3.cloud.ru"
    bucket_name = "test-pastebin"
