from ppm.report import Report
from ppm.sqs import SQSClient
from ppm.backblaze import BackblazeClient
import time
from dotenv import load_dotenv

# Load .env file to the environment variables of the process
load_dotenv('.env')

# Send message through SQS
SQSClient.send_message(
    queue_name='staging-chunk-processed',
    message='JSON FILE'
)

def on_message(message: str):
    Report.event('Message received', message=message)

# Listen messages
SQSClient.launch_queue_consumer(
    queue_name='staging-chunk-to-process',
    on_message=on_message,  # Function that will be executed in each message received.
    block=True,             # Block the thread.
)