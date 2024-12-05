import boto3
from botocore.client import Config

MINIO_CLIENT = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="test_minio_lr4_key_id",
    aws_secret_access_key="test_minio_lr4_key_id_access_key",
    config=Config(signature_version="s3v4"),
)


BUCKET_NAME = "polina"