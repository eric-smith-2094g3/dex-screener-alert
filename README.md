# dex-screener-alert

I needed a simple script to run in the background on my machine that monitors specific Solana and Ethereum pairs on DexScreener and pings my Discord or Telegram when they pump, dump, or cross a target price. Most existing bots are commercial or complex, so I wrote this.

It polls the public DexScreener API and maintains a local state file to avoid spamming alerts. It runs on a loop with a customizable interval.

## Installation

Clone the repository and install the dependencies:

```cmd
pip install -r requirements.txt
```

## Configuration

By default, the tool looks for a `config.json` file in your `%APPDATA%\dex_screener_alert` directory (or you can specify one using `--config`).

Example configuration:

```json
{
  "discord_webhook": "https://discord.com/api/webhooks/12345/abcde",
  "telegram_token": "123456:ABC-DEF1234ghIkl-zyx",
  "telegram_chat_id": "-100123456789",
  "pairs": [
    {
      "chain": "solana",
      "address": "8s98M3bG7H6x9...",
      "rules": [
        { "type": "price_above", "value": 0.15, "cooldown": 3600 },
        { "type": "price_below", "value": 0.08, "cooldown": 3600 },
        { "type": "change_5m_above", "value": 5.5, "cooldown": 600 }
      ]
    }
  ]
}
```

### Supported Rule Types

- `price_above` / `price_below`: Triggered if the USD price goes beyond the target.
- `change_5m_above` / `change_5m_below`: Triggered based on 5-minute price percentage change.
- `change_1h_above` / `change_1h_below`: Triggered based on 1-hour price percentage change.
- `change_6h_above` / `change_6h_below`: Triggered based on 6-hour price percentage change.
- `volume_24h_above`: Triggered if the 24-hour volume in USD exceeds the target.

Each rule can have a optional `cooldown` parameter in seconds (default is 7200 seconds / 2 hours) to prevent continuous alert pings on every loop.

## How to Run

Run the loop with the default 60-second polling interval:

```cmd
python monitor.py
```

Or specify a custom configuration file and interval:

```cmd
python monitor.py --config C:\path\to\my_config.json --interval 120
```

To run a single check and exit immediately (useful for scheduling with Windows Task Scheduler):

```cmd
python monitor.py --once
```

<!-- last-checked: 2026-10-07 -->
