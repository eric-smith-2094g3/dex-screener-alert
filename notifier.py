import time
import httpx

class Notifier:
    def __init__(self, discord_url=None, telegram_token=None, telegram_chat_id=None):
        self.discord_url = discord_url
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self._last_sent = {}  # service name to timestamp

    def _wait_for_cooldown(self, service: str, delay: float = 1.5):
        # Prevent hitting discord/telegram rate limits if polled frequently
        now = time.time()
        last = self._last_sent.get(service, 0.0)
        elapsed = now - last
        if elapsed < delay:
            time.sleep(delay - elapsed)
        self._last_sent[service] = time.time()

    def send_discord(self, message: str):
        if not self.discord_url:
            return
        
        self._wait_for_cooldown("discord")
        payload = {"content": message}
        # print(f"DEBUG payload: {payload}")
        
        # FIXME: discord fails if content is > 2000 chars, truncate just in case
        if len(message) > 1950:
            payload["content"] = message[:1950] + "..."

        r = httpx.post(self.discord_url, json=payload, timeout=10.0)
        r.raise_for_status()

    def send_telegram(self, message: str):
        if not self.telegram_token or not self.telegram_chat_id:
            return

        self._wait_for_cooldown("telegram", delay=2.0)
        
        # Using camelCase here to match the old external script I copied this from
        telegramUrl = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        r = httpx.post(telegramUrl, json=payload, timeout=10.0)
        r.raise_for_status()
