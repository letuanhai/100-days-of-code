from collections import namedtuple
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


# setup web driver
chrome_driver_path = (
    r"C:\Users\hai.letuan\lth-portable-apps\chromedriver_win32\chromedriver.exe"
)
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# goto page
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# find cookie elem
cookie = driver.find_element(By.ID, "cookie")


# check store every 5 seconds and buy most expensive available items
StoreItem = namedtuple("StoreItem", ["elem", "name", "price"])


def get_available_items():
    store = driver.find_element(By.ID, "store")
    store_items = store.find_elements(By.TAG_NAME, "div")
    available_items = []

    for item in store_items:
        if "grayed" not in item.get_attribute(
            "class"
        ) and "display: none" not in item.get_attribute("style"):
            name, price = item.find_element(By.TAG_NAME, "b").text.split(" - ")
            available_items.append(StoreItem(item, name, int(price.replace(",", ""))))

    return available_items


def get_available_items2():
    store_items = driver.find_elements(By.CSS_SELECTOR, "#store b")
    available_items = []

    for item in store_items:
        parent_item = item.find_element(By.XPATH, "..")
        if "grayed" not in parent_item.get_attribute(
            "class"
        ) and "display: none" not in parent_item.get_attribute("style"):
            name, price = item.text.split(" - ")
            available_items.append(StoreItem(item, name, int(price.replace(",", ""))))

    return available_items


# main logic
start_time = time.time()
print(f"start_time: {start_time}")
stop_time = start_time + 5 * 60  # stop after 5 mins
print(f"stop_time: {stop_time}")

while True:
    cookie.click()

    if time.time() > start_time + 5:
        store_items = get_available_items2()
        if store_items:
            best_item = max(store_items, key=lambda x: x.price)
            best_item.elem.click()
        print(f"new start_time: {start_time}")

        start_time += 5

    if time.time() > stop_time:
        cps = driver.find_element(By.ID, "cps")
        print(f"cps: {cps.text}")
        break


driver.quit()
