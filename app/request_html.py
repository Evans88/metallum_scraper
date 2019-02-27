from requests import get
from requests import RequestException
from contextlib import closing
import logging

def get_raw_html(url):
    try:
        with closing(get(url)) as resp:
            content_type = resp.headers.get("Content-Type")
            status_code = resp.status_code

            if content_type.find("html") > -1 and status_code == 200:
                return resp.content
            return None

    except RequestException as e:
        logging.warning(f"Error during request to {url} : {e}")


get_raw_html("https://docs.python.org/2/library/contextlib.html")

