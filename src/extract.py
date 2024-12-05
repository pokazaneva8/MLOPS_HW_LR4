import sys


from src.minio_client import MINIO_CLIENT, BUCKET_NAME

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python extract.py <object_name> <name_file> ")
        sys.exit(1)

    file_name = sys.argv[1]
    save_file = sys.argv[2]
    MINIO_CLIENT.download_file(BUCKET_NAME, file_name, save_file)
