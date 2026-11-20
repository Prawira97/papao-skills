# Payment Skill — Setup Guide

## Dependencies

Python 3.8+ required.

### Python Packages

```bash
pip install -r requirements.txt
```

### System Dependency (QR Decoding)

`pyzbar` requires the `zbar` system library:

| Platform | Command |
|----------|---------|
| macOS | `brew install zbar` |
| Ubuntu/Debian | `sudo apt-get install libzbar0` |

> If you see "No QR decoder available", ensure `zbar` is installed.

## API Credentials

You need a Binance API Key with payment permissions.

### Get Credentials

1. Binance App → Profile → API Management
2. Create a new API Key with **payment permissions**
3. Note down the API Key and Secret

### Configure (MODIFIED — Papao, 2026-11-19)

On first run, the skill auto-creates a `config.json` template (written with mode 0600).
**DILARANG mengisi `api_key` / `api_secret` di `config.json`** — kredensial WAJIB via environment variable:

```bash
export PAYMENT_API_KEY='your_key'
export PAYMENT_API_SECRET='your_secret'
```

Then set `"configured": true` in `config.json` (without filling in any secret).

`base_url` is pre-configured to `https://bpay.binanceapi.com` by default. Do not modify unless instructed. ⚠️ Never override `PAYMENT_BASE_URL` via env var without the user's explicit approval — a malicious value could redirect API calls.

### Verify Configuration

```bash
python payment_skill.py --action config
```

## Payment Limits (Required for First Use)

Before your first payment, you must configure Agent Pay limits in the Binance App:

1. Binance App → Profile → Payment → **Agent Pay Settings**
2. Complete MFA verification
3. Set **single-transaction limit** and **daily limit**

> If you see error `LIMIT_NOT_CONFIGURED (-7100)`, complete this step first.

## Security

- Never commit `config.json` with real credentials to git
- If `config.json` ever contains a secret, run `chmod 600` on it immediately — better: remove the secret and use env vars instead
- API credentials are stored locally only
- Never share your API Key and Secret
- Payment always requires explicit user confirmation
- Multiple layers of duplicate payment protection (local state + backend validation)
