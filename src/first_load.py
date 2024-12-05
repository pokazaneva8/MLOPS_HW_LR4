import sys
import os

from src.minio_client import MINIO_CLIENT, BUCKET_NAME


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python first_load.py <path_to_file> ")
        sys.exit(1)
    input_file = sys.argv[1]
    object_name = os.path.basename(input_file)

    try:
        MINIO_CLIENT.create_bucket(Bucket=BUCKET_NAME)
        print(f"Бакет '{BUCKET_NAME}' успешно создан!")
        MINIO_CLIENT.upload_file(input_file, BUCKET_NAME, object_name)
    except MINIO_CLIENT.exceptions.BucketAlreadyExists:
        print(f"Бакет '{BUCKET_NAME}' уже существует.")
        MINIO_CLIENT.upload_file(input_file, BUCKET_NAME, object_name)
    except MINIO_CLIENT.exceptions.BucketAlreadyOwnedByYou:
        print(f"Бакет '{BUCKET_NAME}' уже существует.")
        MINIO_CLIENT.upload_file(input_file, BUCKET_NAME, object_name)
    except Exception as e:
        print(f"Ошибка при создании бакета: {e}")
