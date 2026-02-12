# Social Media Management Bot

A compliant social media automation tool with rate limiting, consent management, and analytics.

## ⚠️ IMPORTANT DISCLAIMER

This bot is designed for **legitimate marketing only** with explicit consent from group/channel admins.

**You MUST:**
- ✓ Obtain explicit permission from group admins before posting
- ✓ Respect platform rate limits (built-in)
- ✓ Follow each platform's Terms of Service
- ✓ Provide value to communities, not spam

**You MUST NOT:**
- ✗ Use this for spam or unsolicited messages
- ✗ Attempt to evade platform security measures
- ✗ Send messages to non-approved groups
- ✗ Violate any platform's Terms of Service

## Features

- ✅ **Rate Limiting**: Configurable delays between messages
- ✅ **Consent Management**: Only posts to approved groups
- ✅ **Message Validation**: Blocks spam keywords
- ✅ **Daily Limits**: Prevents over-posting
- ✅ **Analytics**: Track campaign performance
- ✅ **Scheduling**: Schedule posts for optimal times
- ✅ **Multi-Platform**: Telegram, Facebook, Instagram

## Installation

```bash
cd social_media_bot
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials

3. Get Telegram Bot Token:
   - Message @BotFather on Telegram
   - Send `/newbot`
   - Copy the token to `.env`

## Usage

### Run the Bot

```bash
python social_bot.py
```

### Available Commands

1. **Add Approved Group**: Register a group with admin consent
2. **Create Campaign**: Set up a messaging campaign
3. **Execute Campaign**: Send messages immediately
4. **View Analytics**: See campaign statistics
5. **List Campaigns**: View all campaigns
6. **Start Scheduler**: Run automated scheduling

### Example Workflow

```
# 1. Add a group (with admin approval)
> Add approved group
Platform: telegram
Group ID: @tech_trading_group
Admin contact: @groupadmin

# 2. Create a campaign
> Create campaign
Platform: telegram
Target groups: @tech_trading_group,@webdev_chat
Message: Check out my portfolio at baro.dev for professional bot development!
Rate limit: 120
Daily limit: 20

# 3. Execute
> Execute campaign
Campaign ID: telegram_1234567890
```

## Rate Limits (Built-in)

| Platform | Min Delay | Daily Max | Notes |
|----------|-----------|-----------|-------|
| Telegram | 60 sec | 50 msgs | Respects flood limits |
| Facebook | 120 sec | 30 msgs | Requires app approval |
| Instagram | 180 sec | 20 msgs | Use with caution |

## Target Categories

The bot focuses on these niches:
- **Tech**: Programming, web development, software
- **Trading**: Crypto, forex, investment
- **Bots**: Automation, API, Telegram/Discord bots

## Admin Panel Integration

Access the admin panel at:
```
https://yourdomain.com/admin
```

Default credentials:
- Username: `admin`
- Password: `baro2025`

## Compliance Features

### Message Validation
Automatically blocks messages containing:
- Spam keywords
- Excessive capitalization (>50%)
- Messages >1000 characters

### Group Approval Required
All target groups must be pre-approved with admin contact information.

### Rate Limiting
Configurable delays prevent hitting platform limits:
```python
rate_limit_seconds = 60  # Minimum 60 seconds between messages
daily_limit = 50         # Maximum 50 messages per day
```

## Logging

All activity is logged to `social_bot.log`:
- Message sends
- Rate limit triggers
- Failed attempts
- Campaign completions

## Troubleshooting

### "Group not approved" error
You must add the group using option 1 before sending messages.

### Rate limit exceeded
The bot enforces delays. Wait for the specified time.

### Daily limit reached
Wait until tomorrow or increase limit in campaign settings.

## Legal Notice

Users are responsible for:
- Complying with platform Terms of Service
- Obtaining necessary permissions
- Respecting community rules
- Following anti-spam laws (CAN-SPAM, GDPR, etc.)

The developer is not responsible for misuse of this tool.

## Support

For issues or questions:
- Email: hi@baro.dev
- WhatsApp: +234 816 992 7034
