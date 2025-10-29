from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    """
    Custom file storage to handle media files in S3 bucket.
    This class extends S3Boto3Storage to provide custom file storage functionality.
    """
    location = 'media'
    file_overwrite = False
    default_acl = 'private'
    
    def __init__(self, *args, **kwargs):
        kwargs['endpoint_url'] = f'https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com'
        super().__init__(*args, **kwargs)

def upload_to_s3(file, file_name):
    """
    Upload a file to S3 bucket
    
    Args:
        file: The file to be uploaded
        file_name: The name to be given to the file in S3
        
    Returns:
        str: The URL of the uploaded file
    """
    storage = MediaStorage()
    file_name = storage.get_available_name(file_name)
    storage.save(file_name, file)
    return storage.url(file_name)