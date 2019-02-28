from app import request_html
from bs4 import BeautifulSoup


main_a = 'https://www.metal-archives.com/lists/A'


html = request_html.get_raw_html(main_a)
soup = BeautifulSoup(html, 'html.parser')