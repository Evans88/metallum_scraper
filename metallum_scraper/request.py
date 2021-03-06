from requests import get
from requests import RequestException
from contextlib import closing
import logging


def get_raw(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    try:
        with closing(get(url, timeout=10, headers=headers)) as resp:
            status_code = resp.status_code

            if status_code == 200:
                return resp.content
            return None

    except RequestException as e:
        logging.warning(f"Error during request to {url} : {e}")



