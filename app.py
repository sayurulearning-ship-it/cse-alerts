import urllib.request
import urllib.parse
import json
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from datetime import datetime

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
    return price

# Streamlit UI
st.title(f"📊 {SYMBOL} Price Monitor")
st.write(f"**Target Price:** {TARGET_PRICE} LKR")

# Automatically check price on every page load
try:
    with st.spinner("Checking price..."):
        price = check_price()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.metric(
            label="Current Price",
            value=f"{price} LKR",
            delta=f"{price - TARGET_PRICE:.2f}"
        )
        
        if price > TARGET_PRICE:
            send_email_alert(price)
            st.success(f"✅ ALERT SENT! Price is above target.")
        else:
            st.info(f"ℹ️ No alert — price is below target")
        
        st.text(f"Last checked: {current_time}")
        
except Exception as e:
    st.error(f"Error: {str(e)}")

st.divider()
st.caption("💡 This app checks the price automatically on every page load. Set up UptimeRobot to ping this URL every 5 minutes.")
