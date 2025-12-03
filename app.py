import streamlit as st
import urllib.request
import urllib.parse
import json
import smtplib
from email.mime.text import MIMEText

# -------- HARD-CODED VALUES ---------
SYMBOL = "CITH.N0000"
TARGET_PRICE = 3.5

SMTP_EMAIL = "dmdsnd.alerts@gmail.com"
SMTP_PASSWORD = "sjwthobkcorwplyf"  # Gmail App Password
TO_EMAIL = "dmdsnd.alerts@gmail.com"
# -----------------------------------


def send_email_alert(symbol, last_price):
    subject = f"{symbol} Price Alert!"
    body = f"{symbol} last traded price is {last_price} LKR, higher than target {TARGET_PRICE} LKR."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = TO_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)


def fetch_price():
    base_url = "https://www.cse.lk/api/"
    endpoint = "companyInfoSummery"
    data = {"symbol": SYMBOL}

    data_encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(base_url + endpoint, data=data_encoded, method="POST")

    with urllib.request.urlopen(req) as response:
        resp = json.loads(response.read().decode("utf-8"))

    symbol_info = resp["reqSymbolInfo"]
    return float(symbol_info["lastTradedPrice"]), SYMBOL


# ---------------- STREAMLIT ROUTE ----------------
st.set_page_config(page_title="Stock Alert API", layout="wide")

# This acts like an API GET endpoint
if st.experimental_get_query_params().get("check", [""])[0] == "1":
    last_price, symbol = fetch_price()

    result = {
        "symbol": symbol,
        "last_traded_price": last_price,
        "target_price": TARGET_PRICE,
        "alert": last_price > TARGET_PRICE
    }

    # Send email if condition matches
    if last_price > TARGET_PRICE:
        send_email_alert(symbol, last_price)

    st.json(result)

else:
    st.write("Use `?check=1` to fetch the stock price.")
