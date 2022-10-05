from typing import Optional
import urllib.request

# url: Public url to download the file
# file_path: Example '../video0.mp4'
def download_file(public_url: str, file_path: Optional[str]=None):
    '''Download a file from a public url.'''
    if file_path is None:
        file_path = public_url.split('/')[-1]
    urllib.request.urlretrieve(public_url, file_path)
