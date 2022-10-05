from typing import Callable, Dict, Tuple, Union
from threading import Lock, Thread
from ppm.report import Report
from ppm.boto3 import Boto3Clients
from ppm.log import setup_logging

# This class has been made following this tutorial: https://www.learnaws.org/2020/12/17/aws-sqs-boto3-guide/
class SQSClient:
    LOCK = Lock()

    # For cache
    _instance = None
    _from_queue_name_to_queue_url: Dict[str, str] = dict()

    @classmethod
    def get_client(cls):
        return Boto3Clients.get_sqs_client()

    @classmethod
    def _create_queue(cls, queue_name: str) -> str:
        sqs_client = cls.get_client()
        response = sqs_client.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '0',
                'VisibilityTimeout': '60',
            }
        )
        return response['QueueUrl']

    @classmethod
    def _fetch_queue_url(cls, queue_name: str):
        response = cls.get_client().get_queue_url(
            QueueName=queue_name,
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
        return response['QueueUrl']

    @classmethod
    def queue_url_from_queue_name(cls, queue_name: str) -> str:
        with cls.LOCK:
            if queue_name not in cls._from_queue_name_to_queue_url:
                try:
                    queue_url = cls._fetch_queue_url(queue_name)
                except Exception:    # TODO: Import SQS.Client.exceptions.QueueDoesNotExist and use it here.
                    # Create queue if does not exist
                    queue_url = cls._create_queue(queue_name=queue_name)

                # Store in in-memory cache
                cls._from_queue_name_to_queue_url[queue_name] = queue_url
        
        # Use cache
        return cls._from_queue_name_to_queue_url[queue_name]

    @classmethod
    def send_message(cls, queue_name: str, message: str):
        sqs_client = cls.get_client()

        queue_url = cls.queue_url_from_queue_name(queue_name)

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    @classmethod
    def delete_message(cls, queue_name: str, receipt_handle: str):
        queue_url = cls.queue_url_from_queue_name(queue_name)

        sqs_client = cls.get_client()
        response = sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle,
        )
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    @classmethod
    def receive_message(cls, queue_name: str, wait_time_seconds: int = 10) -> Union[Tuple[str, str], None]:
        # Must be >= 0 and <= 20
        assert wait_time_seconds >= 0 and wait_time_seconds <= 20

        queue_url = cls.queue_url_from_queue_name(queue_name)

        sqs_client = cls.get_client()
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=wait_time_seconds,
        )

        messages = response.get('Messages', [])
        if len(messages) == 1:
            message = messages[0]
            receipt_handle = message.get('ReceiptHandle', None)
            assert receipt_handle # TODO: Better exception
            body = message.get("Body", None)
            assert body           # TODO: Better exception
            return body, receipt_handle
        elif len(messages) == 0:
            return None
        else:
            raise AssertionError()

    @classmethod
    def queue_consumer(cls, queue_name: str, on_message: Callable[[str, ], None]):
        try:
            # Infinite loop
            while True:
                body_and_receipt_handle = cls.receive_message(queue_name=queue_name)
                if body_and_receipt_handle:
                    # Deconstruct
                    body, receipt_handle = body_and_receipt_handle

                    # Define variable
                    should_requeue_message = True

                    # Call on_message callback
                    try:
                        # Execute function
                        on_message(body)
                        
                        # All is good, do not requeue the message
                        should_requeue_message = False
                    except Exception as e:
                        Report.exception(e, queue_name=queue_name, place=on_message.__name__, next='We are going to requeue the SQS message.', body=body)
                    finally:
                        # Maybe requeue it
                        if should_requeue_message:
                            cls.send_message(queue_name=queue_name, message=body)

                            # Report once
                            Report.event_once('Requeing message', body=body)
                        
                        # Delete received message out of the queue
                        cls.delete_message(queue_name=queue_name, receipt_handle=receipt_handle)
                        
                        # Report once
                        Report.event_once('SQS message deleted from queue.', receipt_handle=receipt_handle, body=body)
        except Exception as e:
            # Report exception
            Report.exception(e, place='SQS queue_consumer', queue_name=queue_name, next='We are going to finish this queue_consumer.')

    @classmethod
    def launch_queue_consumer(cls, queue_name: str, on_message: Callable[[str, ], None], block: bool = False):
        # Launch thread with queue_consumer loop
        fun = lambda: cls.queue_consumer(queue_name=queue_name, on_message=on_message)
        if block:
            fun()
        else:
            Thread(target=fun).start()
