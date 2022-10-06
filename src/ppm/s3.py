from typing import Dict
from ppm.boto3 import Boto3Clients
import os


class S3Client:
    @classmethod
    def s3_client(cls):
        return Boto3Clients.get_s3_client()

    @classmethod
    def download_file(cls, bucket_name: str, object_key: str, file_name: str):
        '''This downloads directly from s3.
        file_name: The local file that will be generated.
        '''
        return cls.s3_client().download_file(bucket_name, object_key, file_name)

    @classmethod
    def change_storage_class(
        cls,
        bucket_name: str,
        object_key: str,
        storage_class: str,
        ):
        '''Source: https://stackoverflow.com/questions/39309846/how-to-change-storage-class-of-existing-key-via-boto3
        storage_class could be: 'STANDARD'|'REDUCED_REDUNDANCY'|'STANDARD_IA'|'ONEZONE_IA'|'INTELLIGENT_TIERING'|'GLACIER'|'DEEP_ARCHIVE'|'OUTPOSTS'|'GLACIER_IR'
        '''
        client = cls.s3_client()
        client.copy({
                'Bucket': bucket_name,
                'Key': object_key,
            },
            bucket_name,
            object_key,
            ExtraArgs = {
                'StorageClass': storage_class,
                'MetadataDirective': 'COPY'
            }
        )

    @classmethod
    def upload_file(cls,
        file_path: str,
        bucket_name: str,
        object_key: str,
        public_acl: bool=True,
        link_expiration_time: int = 24 * 60 * 60,
        ):
        '''
        Source:
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
        file_name: The local filepath of the file you want to upload.
        object_key is the path inside the bucket. For instance: 'cameras/01:23:45:67:89:AB/video0.mp4'
        
        Returns the url of the object.
        If public_acl = True, the url will be public forever. Else, link_expiration_time (in seconds)
        will indicate how much time the url will be public.
        '''
        
        # If S3 object_name was not specified, use file_name
        if object_key is None:
            object_key = os.path.basename(file_path)

        # Get the client
        client = cls.s3_client()

        # Extra args
        extra_args: Dict[str, str] = dict()
        if public_acl:
            extra_args['ACL'] = 'public-read'

        # Upload the file to s3
        client.upload_file(file_path, bucket_name, object_key, ExtraArgs=extra_args)

        if public_acl:
            # The url will be permanent
            return f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
        else:
            # Generate and return temporary URL of uploaded object
            params = {'Bucket': bucket_name, 'Key': object_key}
            expiration = link_expiration_time
            public_url: str = client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expiration,
            )

        return public_url
    
    @classmethod
    def get_all(cls, bucket_name: str):
        '''
        This could be use like so:
        for obj in S3Client.get_all('bucket-name'):
            obj.delete()
        '''
        s3 = Boto3Clients.Resources.s3()
        bucket = s3.Bucket(bucket_name)
        return bucket.objects.all()

