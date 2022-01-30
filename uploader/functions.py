from django.conf import settings

from minio import Minio


minioClient = Minio(settings.MINIO_STORAGE_ENDPOINT,
                    access_key=settings.MINIO_STORAGE_ACCESS_KEY,
                    secret_key=settings.MINIO_STORAGE_SECRET_KEY,
                    secure=False)


def delete_from_minio(file_name, bucket_name=settings.MINIO_STORAGE_MEDIA_BUCKET_NAME):
    minioClient.remove_object(bucket_name, file_name)
