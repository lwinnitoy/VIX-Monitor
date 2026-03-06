"""
VIX Monitor - Automated notification system for DCA buy signals
Checks VIX daily and sends notifications when thresholds are met
"""

import yfinance as yf
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
VIX_THRESHOLDS = {
    30: 1.0,  # VIX 30-39: Buy 1 month worth
    40: 2.0,  # VIX 40-49: Buy 2 months worth
}

COOLDOWN_DAYS = 30  # Days between VIX-triggered purchases
LAST_PURCHASE_FILE = "last_purchase.json"

def get_vix():
    """Fetch current VIX value"""
    try:
        vix = yf.Ticker("^VIX")
        data = vix.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1]
        return None
    except Exception as e:
        print(f"Error fetching VIX: {e}")
        return None

def get_last_purchase_date():
    """Load last purchase date from file"""
    if os.path.exists(LAST_PURCHASE_FILE):
        try:
            with open(LAST_PURCHASE_FILE, 'r') as f:
                data = json.load(f)
                date_str = data.get('date')
                if not date_str:
                    return None
                dt = datetime.fromisoformat(date_str)
                # If stored datetime is naive, assume America/Los_Angeles
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=ZoneInfo('America/Los_Angeles'))
                return dt.astimezone(ZoneInfo('America/Los_Angeles'))
        except Exception:
            return None
    return None

def save_purchase_date():
    """Save current date as last purchase date"""
    now = datetime.now(ZoneInfo('America/Los_Angeles'))
    with open(LAST_PURCHASE_FILE, 'w') as f:
        json.dump({'date': now.isoformat()}, f)

def is_cooldown_active():
    """Check if we're still in cooldown period"""
    last_purchase = get_last_purchase_date()
    if last_purchase is None:
        return False

    now = datetime.now(ZoneInfo('America/Los_Angeles'))
    days_since = (now - last_purchase).days
    return days_since < COOLDOWN_DAYS

def calculate_buy_amount(vix_value):
    """Determine how many months to buy based on VIX"""
    for threshold in sorted(VIX_THRESHOLDS.keys(), reverse=True):
        if vix_value >= threshold:
            return VIX_THRESHOLDS[threshold]
    return 0

def send_email_notification(vix_value, buy_amount):
    """Send email notification via Gmail"""
    # Email configuration - SET THESE ENVIRONMENT VARIABLES
    sender_email = os.environ.get('EMAIL_SENDER')
    sender_password = os.environ.get('EMAIL_PASSWORD')  # Use App Password for Gmail
    receiver_email = os.environ.get('EMAIL_RECEIVER')

    # Ensure all credentials are present and not None
    if not sender_email or not sender_password or not receiver_email:
        print("Email credentials not configured. Set EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER")
        return False

    # All credentials are guaranteed to be str here
    
    subject = f"🚨 VIX Alert: Time to Buy! (VIX: {vix_value:.2f})"
    
    body = f"""
VIX BUYING OPPORTUNITY DETECTED

Current VIX: {vix_value:.2f}
Recommended Action: Buy {buy_amount} month(s) worth from your 20% reserve

Strategy Details:
- VIX 25-29: Buy 0.5 months
- VIX 30-39: Buy 1 month
- VIX 40-49: Buy 2 months
- VIX 50+: Buy 3 months

Next steps:
1. Log into Wealthsimple
2. Purchase {buy_amount} month(s) worth of your target ETFs
3. Update your tracking spreadsheet

This notification has a {COOLDOWN_DAYS}-day cooldown. You won't receive another alert until the cooldown expires.

---
Automated VIX Monitor System
{datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Convert to str after checking for None
    sender_email = str(sender_email)
    sender_password = str(sender_password)
    receiver_email = str(receiver_email)

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        print(f"✓ Email sent successfully to {receiver_email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False

def send_discord_notification(vix_value, buy_amount):
    """Send notification via Discord webhook"""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("Discord webhook not configured. Set DISCORD_WEBHOOK_URL")
        return False
    
    import requests
    
    message = {
        "content": f"🚨 **VIX ALERT** 🚨\n\n"
                   f"Current VIX: **{vix_value:.2f}**\n"
                   f"Action: Buy **{buy_amount} month(s)** worth from reserve\n\n"
                   f"Log into Wealthsimple and execute your purchase!"
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code == 204:
            print("✓ Discord notification sent")
            return True
        else:
            print(f"✗ Discord notification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to send Discord notification: {e}")
        return False

def main():
    """Main monitoring logic"""
    print(f"\n{'='*50}")
    print(f"VIX Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # Check cooldown
    if is_cooldown_active():
        last_purchase = get_last_purchase_date()
        if last_purchase is not None:
            now = datetime.now(ZoneInfo('America/Los_Angeles'))
            days_remaining = COOLDOWN_DAYS - (now - last_purchase).days
            print(f"⏳ Cooldown active: {days_remaining} days remaining")
            print("   No alerts will be sent until cooldown expires.\n")
        else:
            print("⏳ Cooldown active, but last purchase date is unknown.")
            print("   No alerts will be sent until cooldown expires.\n")
        return
    
    # Fetch VIX
    vix_value = get_vix()
    if vix_value is None:
        print("✗ Failed to fetch VIX data\n")
        return
    
    print(f"Current VIX: {vix_value:.2f}")
    
    # Check thresholds
    buy_amount = calculate_buy_amount(vix_value)
    
    if buy_amount > 0:
        print(f"🎯 TRIGGER: Buy {buy_amount} month(s) worth!")
        print(f"   Sending notifications...\n")
        
        # Send notifications (try both methods)
        email_sent = send_email_notification(vix_value, buy_amount)
        discord_sent = send_discord_notification(vix_value, buy_amount)
        
        if email_sent or discord_sent:
            save_purchase_date()
            print(f"\n✓ Notifications sent. Cooldown active for {COOLDOWN_DAYS} days.")
        else:
            print("\n✗ No notifications were sent (check configuration)")
    else:
        print(f"✓ No action needed (VIX below threshold)")
    
    print()

if __name__ == "__main__":
    main()
