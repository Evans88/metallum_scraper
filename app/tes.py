from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

driver_opts = Options()
driver_opts.add_argument("--headless")

driver = webdriver.Chrome('C:\\Users\\evansdar\\Code\\Python\\metallum_scraper\\app\\driver\\chromedriver.exe', chrome_options=driver_opts)

driver.get("https://www.metal-archives.com/bands/Mg%C5%82a/44722")
#print(driver.page_source)
html = BeautifulSoup(driver.page_source, 'html.parser')

#TODO not sure if this list of css classes is exhaustive

discog_table = html.find("table", {"class": "display discog"})
for i in discog_table.findAll("a", {"class": ["other", "album", "single", "demo"]}, href=True):
    print(i)


"""
a_href = html.findAll("td")
for i in a_href:
    for b in i.findAll("a"):
        print(b)




try:
    myElem = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'other')))

except TimeoutException:
    print("Loading took too much time!")
"""