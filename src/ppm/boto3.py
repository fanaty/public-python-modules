from threading import Lock
import boto3
import botocore.client
from ppm.env import get_env_or_raise

# Source: https://stackoverflow.com/questions/60537479/aws-dynamodb-connection-pools-full-warning
DYNAMODB_MAX_POOL_CONNECTIONS = 200

class Boto3Clients:
    LOCK = Lock()
    _dynamodb_client = None
    _s3_client = None
    _b2_client = None
    _sqs_client = None

    @classmethod
    def get_dynamodb_client(cls):
        # Related: https://github.com/boto/boto3/issues/801
        with cls.LOCK:
            client = cls._dynamodb_client
            if client is None:
                client = boto3.client('dynamodb',
                    aws_access_key_id=get_env_or_raise('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=get_env_or_raise('AWS_SECRET_ACCESS_KEY'),
                    region_name=get_env_or_raise('AWS_DEFAULT_REGION'),
                )
                cls._dynamodb_client = client
            return client

    @classmethod
    def get_s3_client(cls):
        # Related: https://github.com/boto/boto3/issues/801
        with cls.LOCK:
            client = cls._s3_client
            if client is None:
                client = boto3.client('s3',
                    aws_access_key_id=get_env_or_raise('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=get_env_or_raise('AWS_SECRET_ACCESS_KEY'),
                    region_name=get_env_or_raise('AWS_DEFAULT_REGION'),
                )
                cls._s3_client = client
            return client

    # https://www.backblaze.com/b2/docs/python.html
    @classmethod
    def get_b2_client(cls, endpoint_url: str, backblaze_key_id: str, backblaze_application_key: str):
        # Related: https://github.com/boto/boto3/issues/801
        with cls.LOCK:
            client = cls._b2_client
            if client is None:
                client = boto3.client('s3',
                    endpoint_url='https://' + endpoint_url,
                    aws_access_key_id=backblaze_key_id,
                    aws_secret_access_key= backblaze_application_key,
                    region_name='us-west-004',
                )
                cls._b2_client = client
            return client

    @classmethod
    def get_sqs_client(cls):
        # Related: https://github.com/boto/boto3/issues/801
        with cls.LOCK:
            client = cls._sqs_client
            if client is None:
                client = boto3.client('sqs',
                    aws_access_key_id=get_env_or_raise('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=get_env_or_raise('AWS_SECRET_ACCESS_KEY'),
                    region_name=get_env_or_raise('AWS_DEFAULT_REGION'),
                )
                cls._sqs_client = client
            return client

    class Resources:
        @classmethod
        def dynamodb(cls):
            config = botocore.client.Config(max_pool_connections=DYNAMODB_MAX_POOL_CONNECTIONS)

            return boto3.resource('dynamodb', config=config)

        @classmethod
        def s3(cls):
            return boto3.resource('s3')