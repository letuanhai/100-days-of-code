from collections import namedtuple
import smtplib
from email.message import Message
import os
import time

import requests
from bs4 import BeautifulSoup
import dotenv

dotenv.load_dotenv()

ProductItem = namedtuple("ProductItem", ["name", "link", "low_price"])

products = [
    ProductItem(
        name="Giá Đỡ Điện Thoại Di Động HOCO",
        link="https://www.lazada.vn/products/gia-do-dien-thoai-di-dong-hoco-gia-do-may-tinh-de-ban-bang-kim-loai-dieu-chinh-duoc-cho-iphone-ipad-i901360810-s2615478288.html",
        low_price=105_000,
    ),
    ProductItem(
        name="Giá đỡ điện thoại UGREEN LP373",
        link="https://www.lazada.vn/products/i1410484292-s5837592441.html",
        low_price=130_000,
    ),
    ProductItem(
        name="Gối cong Memory Foam Lock&Lock HLW111",
        link="https://www.lazada.vn/products/i103714508-s104619061.html",
        low_price=220_000,
    ),
    ProductItem(
        name="Gối Memory foam 50D Lock&Lock HLW114",
        link="https://www.lazada.vn/products/i100112343-s100145041.html",
        low_price=400_000,
    ),
    ProductItem(
        name="Máy sấy tóc Panasonic EH-ND65-K645",
        link="https://www.lazada.vn/products/i1818868644-s8196662363.html",
        low_price=650_000,
    ),
    ProductItem(
        name="Máy Sấy Tóc Ionity Panasonic EH-NE65",
        link="https://www.lazada.vn/products/i101324003-s6348234427.html",
        low_price=700_000,
    ),
    ProductItem(
        name="Giá Đỡ Máy Tính Xách Tay",
        link="https://www.lazada.vn/products/i1378326664-s5710365273.html",
        low_price=200_000,
    ),
]


class PriceTagNotFoundError(BaseException):
    pass


def check_lazada_price(product_link: str):
    time.sleep(1)
    r = requests.get(url=product_link)
    r.raise_for_status()

    html = r.text

    soup = BeautifulSoup(html, features="lxml")

    price_tag = soup.find(
        "span",
        class_="pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl",
    )

    if price_tag is None:
        raise PriceTagNotFoundError
    price = float(price_tag.text.split(" ")[0].replace(".", ""))
    return price


def send_email(msg: str, to_email: str = os.environ["TO_EMAIL"]):
    email_msg = Message()
    email_msg["Subject"] = "Lazada price alert!!!"
    email_msg["From"] = os.environ["MY_EMAIL"]
    email_msg["To"] = to_email
    email_msg.add_header("Content-Type", "text/html")
    email_msg.set_payload(msg, charset="utf-8")

    with smtplib.SMTP("smtp-mail.outlook.com", port=587) as conn:
        conn.starttls()
        conn.login(user=os.environ["MY_EMAIL"], password=os.environ["MY_EMAIL_PW"])
        conn.sendmail(
            from_addr=email_msg["From"],
            to_addrs=[email_msg["To"]],
            msg=email_msg.as_string(),
        )


for p in products:
    price = check_lazada_price(p.link)
    if price <= p.low_price:
        send_email(
            msg=f"The price of <b>{p.name}</b> has dropped to <b>{price:0,.0f} VND</b>.<br><br>Link: {p.link}"
        )
