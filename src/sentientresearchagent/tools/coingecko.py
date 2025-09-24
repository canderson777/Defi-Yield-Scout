from __future__ import annotations
from typing import Optional
import os, httpx

# Minimal chain->coingecko network slug map for token_price endpoint
_CG_NETWORKS = {
    "ethereum": "ethereum",
    "arbitrum": "arbitrum-one",
    "base": "base",
    "polygon": "polygon-pos",
    "optimism": "optimistic-ethereum",
}

class CoinGeckoClient:
    def __init__(self, timeout=15.0):
        self.key = os.getenv("COINGECKO_API_KEY")
        self.client = httpx.AsyncClient(timeout=timeout)
        self.base = "https://pro-api.coingecko.com/api/v3" if self.key else "https://api.coingecko.com/api/v3"

    async def price_by_token(self, chain: str, token_address: str) -> Optional[float]:
        if not chain or not token_address:
            return None
        # Try contract-price. If no key, fall back to None (keep code simple).
        network = _CG_NETWORKS.get(chain.lower())
        if not network or not self.key:
            return None
        url = f"{self.base}/onchain/simple/networks/{network}/token_price/{token_address}"
        headers = {"x-cg-pro-api-key": self.key} if self.key else {}
        r = await self.client.get(url, headers=headers)
        if r.status_code != 200:
            return None
        data = r.json()
        # API returns {"<address>": {"usd": 1.02, ...}}
        info = data.get(token_address.lower()) or {}
        return info.get("usd")
