import smtplib
import datetime as dt
import random
from collections import namedtuple
import csv

my_email = ""
pw = ""

letter_templates = []
for i in range(1, 4):
    with open(f"./letter_templates/letter_{i}.txt", "r") as f:
        letter_templates.append(f.read())

Record = namedtuple("Record", ["name", "email", "year", "month", "day"])
birthdays = []
with open("./birthdays.csv", "r") as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # skip header row
    for row in csv_reader:
        birthdays.append(Record(*row))


def send_email(to_email: str, msg: str):
    with smtplib.SMTP("smtp-mail.outlook.com", port=587) as conn:
        conn.starttls()
        conn.login(user=my_email, password=pw)
        conn.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg=f"Subject:Happy Birthday\n\n{msg}",
        )


current_date = dt.datetime.now().date()

for r in birthdays:
    if current_date.day == int(r.day) and current_date.month == int(r.month):
        msg = random.choice(letter_templates).replace("[NAME]", r.name)
        send_email(r.email, msg=msg)
