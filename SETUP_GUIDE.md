# VIX Monitor - Complete Setup Guide

## What This Does
Automatically checks VIX daily and sends you notifications when it's time to buy extra from your 20% reserve fund.

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test It Locally
```bash
python vix_monitor.py
```

This will check the current VIX and print output (but won't send notifications until configured).

---

## Notification Setup

Choose one or both notification methods:

### Option A: Email Notifications (Recommended)

**Using Gmail (Free):**

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Copy the 16-character password

3. Set environment variables (on Mac/Linux):
```bash
export EMAIL_SENDER="your.email@gmail.com"
export EMAIL_PASSWORD="your-16-char-app-password"
export EMAIL_RECEIVER="your.email@gmail.com"  # Can be same or different
```

On Windows (PowerShell):
```powershell
$env:EMAIL_SENDER="your.email@gmail.com"
$env:EMAIL_PASSWORD="your-16-char-app-password"
$env:EMAIL_RECEIVER="your.email@gmail.com"
```

### Option B: Discord Notifications (Alternative)

1. Create a Discord server (or use existing)
2. Create a webhook:
   - Server Settings → Integrations → Webhooks → New Webhook
   - Copy the webhook URL

3. Set environment variable:
```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

---

## Hosting Options (Free & Cheap)

### Option 1: PythonAnywhere (FREE - RECOMMENDED FOR BEGINNERS)

**Cost:** Free forever (with limitations)
**Runs:** Daily at scheduled time
**Setup Time:** 15 minutes

**Steps:**
1. Create free account at https://www.pythonanywhere.com
2. Go to "Files" tab, upload `vix_monitor.py` and `requirements.txt`
3. Open a Bash console, run:
   ```bash
   pip install --user -r requirements.txt
   ```
4. Go to "Tasks" tab
5. Create new scheduled task:
   - Time: `14:00` (2pm UTC = 9am EST)
   - Command: `/home/yourusername/vix_monitor.py`
6. Add environment variables in "Files" → `.bashrc`:
   ```bash
   export EMAIL_SENDER="your.email@gmail.com"
   export EMAIL_PASSWORD="your-app-password"
   export EMAIL_RECEIVER="your.email@gmail.com"
   ```

**Pros:** Easiest setup, truly free forever, web interface
**Cons:** Only one scheduled task on free tier, runs once daily

---

### Option 2: GitHub Actions (FREE)

**Cost:** Free for public repos
**Runs:** Any schedule you want (e.g., every 6 hours)
**Setup Time:** 20 minutes

**Steps:**
1. Create GitHub account (if needed)
2. Create new repository, upload your files
3. Add secrets (Settings → Secrets → Actions):
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECEIVER`
4. Create `.github/workflows/vix-monitor.yml`:

```yaml
name: VIX Monitor
on:
  schedule:
    - cron: '0 14 * * *'  # 2pm UTC daily (9am EST)
  workflow_dispatch:  # Manual trigger button

jobs:
  check-vix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python vix_monitor.py
        env:
          EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_RECEIVER: ${{ secrets.EMAIL_RECEIVER }}
```

**Pros:** Free, flexible scheduling, version controlled
**Cons:** Requires GitHub knowledge, public repo (or pay for private)

---

### Option 3: Raspberry Pi / Old Computer (FREE if you have hardware)

**Cost:** Free (electricity ~$1-2/month)
**Runs:** Any schedule, runs locally
**Setup Time:** 30 minutes

**Steps:**
1. Install Python on your device
2. Copy files to a folder (e.g., `/home/pi/vix-monitor/`)
3. Install dependencies: `pip install -r requirements.txt`
4. Add to crontab for daily execution:
   ```bash
   crontab -e
   ```
   Add line:
   ```
   0 9 * * * cd /home/pi/vix-monitor && /usr/bin/python3 vix_monitor.py
   ```
5. Add environment variables to `~/.bashrc`

**Pros:** Complete control, runs locally, private
**Cons:** Requires always-on device, requires hardware

---

### Option 4: Railway.app (FREE $5/month credit)

**Cost:** Free $5/month credit (enough for this)
**Runs:** Can run 24/7 with cron
**Setup Time:** 25 minutes

**Steps:**
1. Create account at https://railway.app
2. Create new project from GitHub repo
3. Add environment variables in dashboard
4. Railway auto-deploys when you push to GitHub

---

### Option 5: Google Cloud Functions (FREE tier generous)

**Cost:** Free up to 2 million invocations/month
**Runs:** Any schedule via Cloud Scheduler
**Setup Time:** 30 minutes

Requires Google Cloud account and some cloud knowledge.

---

### Option 6: Render.com Cron Jobs (FREE)

**Cost:** Free tier available
**Runs:** Scheduled cron jobs
**Setup Time:** 20 minutes

Similar to Railway but specifically designed for scheduled tasks.

---

## My Recommendation

**If you're new to this:** Start with **PythonAnywhere**
- Easiest to set up
- Free forever
- Web interface for everything
- Perfect for daily checks

**If you know GitHub:** Use **GitHub Actions**
- More flexible
- Version controlled
- Easy to modify

**If you have a Raspberry Pi:** Run it locally
- Most reliable
- No external dependencies
- Complete privacy

---

## Customization

Edit the thresholds in `vix_monitor.py`:

```python
VIX_THRESHOLDS = {
    25: 0.5,  # VIX 25-29: Buy 0.5 months worth
    30: 1.0,  # VIX 30-39: Buy 1 month worth
    40: 2.0,  # VIX 40-49: Buy 2 months worth
    50: 3.0   # VIX 50+: Buy 3 months worth
}

COOLDOWN_DAYS = 30  # Days between purchases
```

---

## Testing

Test without triggering cooldown by temporarily commenting out this line:
```python
# save_purchase_date()  # COMMENT THIS OUT FOR TESTING
```

Or manually delete `last_purchase.json` to reset cooldown.

---

## Troubleshooting

**"Failed to fetch VIX data"**
- Check internet connection
- Yahoo Finance API might be temporarily down
- Try again in a few minutes

**"Email credentials not configured"**
- Make sure environment variables are set
- Check for typos in variable names
- Gmail: Verify you're using App Password, not regular password

**"Discord notification failed"**
- Verify webhook URL is correct
- Check Discord server permissions

---

## Security Notes

- Never commit your email password or API keys to GitHub
- Use environment variables or secrets management
- Use Gmail App Passwords, not your main password
- Keep `last_purchase.json` backed up if using local hosting

---

## Next Steps After Setup

1. Test the script manually to ensure notifications work
2. Set up your hosting platform
3. Wait for the first alert
4. When alerted, log into Wealthsimple and execute your buy
5. The system automatically tracks cooldown for you

Good luck with your automated VIX strategy!
