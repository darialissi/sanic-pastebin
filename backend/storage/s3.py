from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from aiobotocore.session import get_session


class AbstractStorage(ABC):

    @abstractmethod
    async def put_object():
        raise NotImplementedError

    @abstractmethod
    async def get_object():
        raise NotImplementedError


class S3Storage(AbstractStorage):
    access_key: str = None
    secret_key: str = None
    region_name: str = None
    endpoint_url: str = None
    bucket_name: str = None

    def __init__(self):
        self.config = {
            "aws_access_key_id": self.access_key,
            "aws_secret_access_key": self.secret_key,
            "region_name": self.region_name,
            "endpoint_url": self.endpoint_url,
        }
        self.bucket_name = self.bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def put_object(self, object_name, body):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=body,
            )

    async def get_object(self, object_name):
        async with self.get_client() as client:
            resp = await client.get_object(
                Bucket=self.bucket_name,
                Key=object_name,
            )
            async with resp["Body"] as stream:
                body = await stream.read()

        return body.decode()
