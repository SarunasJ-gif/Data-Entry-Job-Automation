import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

response = requests.get(url=url, headers=headers)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

object_links = []
links = soup.find_all(name="a", class_="property-card-link")
for link in links:
    object_link = link["href"]
    if "http" not in object_link:
        object_links.append(f"https://www.zillow.com/{object_link}")
    else:
        object_links.append(object_link)

prices = soup.find_all(name="div", class_="StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0 kJFQQX")
object_prices = [price.get_text().split("+")[0].replace("/mo", "") for price in prices if "$" in price.text]

addresses = soup.select(selector="a address")
object_addresses = [address.getText().split(" | ")[-1] for address in addresses]

# ---------------------------------------------------------------------------------------------------------------

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

forms_url = "https://docs.google.com/forms/d/e/SV2_MEpcIYHJ0zjkA/viewform?usp=sf_link"
WEB_DRIVER_PATH = "C:\Development/chromedriver.exe"
driver = webdriver.Chrome(chrome_options=options, executable_path=WEB_DRIVER_PATH)
driver.get(forms_url)

for index, link in enumerate(object_links):
    driver.get(forms_url)
    time.sleep(4)
    if index >= len(object_prices) or index >= len(object_addresses):
        continue
    else:
        print(f"{index + 1}. {object_prices[index]} / {object_addresses[index]}: {link}")
        address_property = driver.find_element(By.XPATH,
                                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_month = driver.find_element(By.XPATH,
                                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_property = driver.find_element(By.XPATH,
                                            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_property.send_keys(object_addresses[index])
        price_month.send_keys(object_prices[index])
        link_property.send_keys(link)
        submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit_button.click()
        next_answer = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        next_answer.click()
