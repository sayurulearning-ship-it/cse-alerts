import urllib.request
import urllib.parse
import json
import smtplib
from email.mime.text import MIMEText

# -------------------------------------------
# Gmail SMTP SETTINGS
# -------------------------------------------
GMAIL_USER = "dmdsnd.alerts@gmail.com"
GMAIL_APP_PASSWORD = "sjwthobkcorwplyf"
TO_EMAIL = "dmdsnd.alerts@gmail.com"

# -------------------------------------------
TARGET_PRICE = 3.5
SYMBOL = "CITH.N0000"

def send_email_alert(price):
    msg = MIMEText(f"Alert! {SYMBOL} price is now {price} LKR (Target: {TARGET_PRICE})")
    msg["Subject"] = f"{SYMBOL} Price Alert"
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)

def check_price():
    base_url = "https://www.cse.lk/api/"
    endpoint = "companyInfoSummery"

    data = {"symbol": SYMBOL}
    encoded = urllib.parse.urlencode(data).encode("utf-8")

    req = urllib.request.Request(base_url + endpoint, data=encoded, method="POST")

    with urllib.request.urlopen(req) as response:
        json_data = json.loads(response.read().decode("utf-8"))

    price = float(json_data["reqSymbolInfo"]["lastTradedPrice"])

    print(f"{SYMBOL}: {price} LKR")

    if price > TARGET_PRICE:
        send_email_alert(price)
        print("ALERT SENT")
    else:
        print("No alert — price below target")

# Run the function
check_price()
