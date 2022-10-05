from typing import Dict, Optional
from ppm.env import get_env_or_raise
from ppm.boto3 import Boto3Clients
import os

class BackblazeClient:
    @classmethod
    def upload_file(cls, file_path: str, bucket_name: str, object_key: Optional[str]= None, public_acl: bool=True):
        # If S3 object_name was not specified, use file_name
        if object_key is None:
            object_key = os.path.basename(file_path)
        
        # Upload the file
        client = Boto3Clients.get_b2_client(
            endpoint_url=get_env_or_raise('BACKBLAZE_ENDPOINT'),
            backblaze_key_id=get_env_or_raise('BACKBLAZE_KEY_ID'),
            backblaze_application_key=get_env_or_raise('BACKBLAZE_APPLICATION_KEY'),
        )

        # Extra args
        extra_args: Dict[str, str] = dict()
        if public_acl:
            extra_args['ACL'] = 'public-read'

        # Upload the file to s3
        client.upload_file(file_path, bucket_name, object_key, ExtraArgs=extra_args)

        if public_acl:
            # The url will be permanent
            return f'https://{bucket_name}.s3.us-west-004.backblazeb2.com/{object_key}'
        else:
            # Generate and return temporary URL of uploaded object
            params = {'Bucket': bucket_name, 'Key': object_key}
            expiration = 24 * 60 * 60   # In seconds. 
            public_url: str = client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expiration,
            )

        return public_url