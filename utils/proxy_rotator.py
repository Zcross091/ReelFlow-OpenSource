import os
import itertools
import logging
log = logging.getLogger(__name__)
# Load proxies from .env
_raw = os.getenv("INSTAGRAM_PROXIES") or os.getenv("INSTAGRAM_PROXY") or ""
PROXY_LIST = [p.strip() for p in _raw.split(",") if p.strip()]
_cycle = itertools.cycle(PROXY_LIST) if PROXY_LIST else None
def get_next_proxy() -> str | None:
    """Return next proxy in rotation"""
    if not _cycle:
        return None
    return next(_cycle)
def apply_next_proxy(cl) -> str | None:
    """Apply next proxy to instagrapi client"""
    proxy = get_next_proxy()
    if proxy:
        cl.set_proxy(proxy)
        # Hide credentials in logs
        display = proxy.split("@")[-1] if "@" in proxy else proxy
        log.info(f"🔄 Switched proxy → {display}")
    return proxy
