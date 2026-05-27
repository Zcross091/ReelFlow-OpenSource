# anime-ig-reposter-bot

This bot posts anime clips to Instagram using `instagrapi` and supports loading saved sessions from `session.json`.

## Environment setup

1. Copy `.env.example` to `.env`.
2. Set your Instagram credentials:

```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

3. If Instagram blocks your server IP, add your Termux HTTP proxy URL:

```env
INSTAGRAM_PROXY=http://user:password@proxy_ip:proxy_port
```

For a Termux proxy, use the HTTP proxy address shown in Termux and include credentials if required.

## Run

```bash
python bot.py
```

If login fails due to security checks, open Instagram manually or try the proxy URL again.
