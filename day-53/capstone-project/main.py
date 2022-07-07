from collections import namedtuple
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By


Item = namedtuple(
    "Item", ["title", "price", "size", "location", "description", "post_date"]
)

# setup web driver
chrome_driver_path = (
    r"C:\Users\hai.letuan\lth-portable-apps\chromedriver_win32\chromedriver.exe"
)

BASE_URL = "https://batdongsan.com.vn/cho-thue-can-ho-chung-cu-ba-dinh/gia-tu-5-trieu-den-10-trieu-dt-tu-30m2-den-50m2"

all_items = []

for i in range(1, 6):

    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    url = BASE_URL if i == 1 else BASE_URL + f"/p{i}"

    driver.get(url)

    for el in driver.find_elements(By.CSS_SELECTOR, ".js__card.js__card-full-web"):
        title = el.find_element(By.CSS_SELECTOR, "h3.re__card-title").text
        price = el.find_element(By.CSS_SELECTOR, ".re__card-config-price").text
        size = el.find_element(By.CSS_SELECTOR, ".re__card-config-area").text
        location = el.find_element(By.CSS_SELECTOR, ".re__card-location").text
        desc = el.find_element(By.CSS_SELECTOR, ".re__card-description").text
        post_date = el.find_element(
            By.CSS_SELECTOR, ".re__card-published-info-published-at"
        ).get_attribute("aria-label")

        new_item = Item(title, price, size, location, desc, post_date)
        all_items.append(new_item)

    driver.quit()

with open("results.csv", "w", encoding="utf-8", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(Item._fields)
    csv_writer.writerows([list(i) for i in all_items])
