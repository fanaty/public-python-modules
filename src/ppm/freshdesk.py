import logging
from typing import List
import requests
import json

class Freshdesk:
    api_key: str
    api_url: str
    HEADERS = {'Content-Type': 'application/json'}  # Extracted from Freshdesk documentation.
    PASSWORD = 'X'                                  # Extracted from Freshdesk documentation.
    
    def __init__(self, api_key: str, subdomain: str) -> None:
        self.api_key = api_key
        self.api_url = f'https://{subdomain}.freshdesk.com/api'
        self.auth = (api_key, self.PASSWORD, )

    def create_ticket(self, subject: str, description: str, email: str, cc_emails: List[str] = [], status: int = 2, priority: int = 3):
        assert description != ''
        url = f'{self.api_url}/v2/tickets'
        data = json.dumps({
            'description': description,
            'subject': subject,
            'email': email,
            'priority': priority,
            'status': status,
            'cc_emails': cc_emails,
        })
        response = requests.post(url=url, data=data, headers=self.HEADERS, auth=self.auth)

        if response.status_code >= 300:
            logging.warn(f'Warning! Freshdesk API. Response content = {response.content}. Status code = {response.status_code}')

        response.raise_for_status()