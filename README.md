# VIX-Enhanced DCA Investment System

Complete automated system for implementing a VIX-triggered dollar-cost averaging strategy.

## 📁 What's Included

### Core Files
- **`vix_monitor.py`** - Main Python script that checks VIX and sends alerts
- **`requirements.txt`** - Python dependencies (yfinance, requests)

### Documentation
- **`VIX_STRATEGY_OUTLINE.md`** - Complete strategy explanation and rationale
- **`SETUP_GUIDE.md`** - Step-by-step setup for hosting and notifications
- **`QUICK_REFERENCE.md`** - Print-friendly quick reference card

## 🚀 Quick Start (5 minutes)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the script:**
   ```bash
   python vix_monitor.py
   ```
   You'll see current VIX value and whether it triggers a buy signal.

3. **Set up notifications** (choose one):
   - Email: Set `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER` environment variables
   - Discord: Set `DISCORD_WEBHOOK_URL` environment variable

4. **Deploy to hosting platform:**
   - See `SETUP_GUIDE.md` for detailed instructions
   - **Recommended for beginners:** PythonAnywhere (free, easy)
   - **Recommended for developers:** GitHub Actions (free, flexible)

## 📊 The Strategy in 30 Seconds

**Regular investing:** 80% of capital divided into monthly purchases

**Opportunistic buying:** 20% reserve deployed when VIX spikes:
- VIX 25-29 → Buy 0.5 months worth
- VIX 30-39 → Buy 1 month worth  
- VIX 40-49 → Buy 2 months worth
- VIX 50+ → Buy 3 months worth

**Safety:** 30-day cooldown between VIX-triggered buys

## 📖 Reading Order

New to this? Read in this order:

1. **`VIX_STRATEGY_OUTLINE.md`** - Understand the strategy
2. **`SETUP_GUIDE.md`** - Set up the automation
3. **`QUICK_REFERENCE.md`** - Keep this handy for daily use

## 🔧 Customization

Edit thresholds in `vix_monitor.py`:

```python
VIX_THRESHOLDS = {
    25: 0.5,  # Your thresholds here
    30: 1.0,
    40: 2.0,
    50: 3.0
}

COOLDOWN_DAYS = 30  # Adjust as needed
```

## 💡 Features

- ✅ Fetches real-time VIX data from Yahoo Finance
- ✅ Graduated buying based on fear levels
- ✅ Automatic cooldown period tracking
- ✅ Multiple notification methods (email, Discord)
- ✅ Detailed logs for every check
- ✅ Prevents overspending during extended volatility
- ✅ Free to run on multiple platforms

## 🎯 Who This Is For

- Long-term investors (10+ year horizon)
- People who want systematic, emotion-free investing
- Those comfortable with ETF investing
- Anyone looking to buy dips without guessing the bottom
- Investors with lump sum capital to deploy strategically

## ⚠️ Important Notes

- This is for **long-term investing**, not day trading
- Past VIX patterns don't guarantee future results
- Always maintain emergency fund separate from this strategy
- This is educational; not financial advice
- Test thoroughly before deploying real capital

## 🆘 Support

Check the `SETUP_GUIDE.md` troubleshooting section for common issues.

## 📝 License

Use freely for personal investing. Not for commercial distribution.

---

**Good luck with your investing! Remember: Time in the market beats timing the market.**
