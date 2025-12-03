import urllib.request
import urllib.parse
import json
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from datetime import datetime
import time

# -------------------------------------------
# Gmail SMTP SETTINGS
# -------------------------------------------
GMAIL_USER = "dmdsnd.alerts@gmail.com"
GMAIL_APP_PASSWORD = "sjwthobkcorwplyf"
TO_EMAIL = "dmdsnd.alerts@gmail.com"

# -------------------------------------------
TARGET_PRICE = 3.5
SYMBOL = "CITH.N0000"
REFRESH_INTERVAL = 300  # Refresh every 5 minutes (300 seconds)

def send_email_alert(price):
    msg = MIMEText(f"Alert! {SYMBOL} price is now {price} LKR (Target: {TARGET_PRICE})")
    msg["Subject"] = f"{SYMBOL} Price Alert - {price} LKR"
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
st.write(f"**Auto-refresh:** Every {REFRESH_INTERVAL} seconds")

# Create placeholder for dynamic content
status_placeholder = st.empty()
price_placeholder = st.empty()
time_placeholder = st.empty()

# Auto-refresh logic
try:
    price = check_price()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Display current price
    price_placeholder.metric(
        label="Current Price",
        value=f"{price} LKR",
        delta=f"{price - TARGET_PRICE:.2f}" if price > TARGET_PRICE else f"{price - TARGET_PRICE:.2f}"
    )
    
    # Check if alert should be sent
    if price > TARGET_PRICE:
        send_email_alert(price)
        status_placeholder.success(f"✅ ALERT SENT! Price is above target.")
    else:
        status_placeholder.info(f"ℹ️ No alert — price is below target")
    
    time_placeholder.text(f"Last checked: {current_time}")
    
except Exception as e:
    st.error(f"Error: {str(e)}")

# Auto-refresh the page
time.sleep(REFRESH_INTERVAL)
st.rerun()
