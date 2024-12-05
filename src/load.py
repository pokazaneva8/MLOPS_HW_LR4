import sys
from botocore.client import Config
from src.minio_client import BUCKET_NAME, MINIO_CLIENT


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python extract.py <object_name> <name_file> ")
        sys.exit(1)

    file_name = sys.argv[1]
    save_file = sys.argv[2]
    MINIO_CLIENT.upload_file(file_name, BUCKET_NAME, save_file)
