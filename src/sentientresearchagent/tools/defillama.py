from __future__ import annotations
from typing import List, Optional, Dict, Any
import httpx

_LLAMA_YIELDS = "https://yields.llama.fi/pools"

class DefiLlamaClient:
    def __init__(self, timeout=30.0):
        self._client = httpx.AsyncClient(timeout=timeout)

    async def fetch_pools(
        self,
        chains: Optional[List[str]] = None,
        projects: Optional[List[str]] = None,
        stablecoin_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of pool dicts with keys like:
         - apy, apyBase, apyReward, tvlUsd, chain, project, symbol, pool, url, underlyingTokens
        """
        r = await self._client.get(_LLAMA_YIELDS)
        r.raise_for_status()
        data = r.json()
        pools = data.get("data") or data.get("pools") or []  # handle schema variance
        def ok(p):
            if chains and (p.get("chain") or "").lower() not in {c.lower() for c in chains}:
                return False
            if projects and (p.get("project") or "").lower() not in {x.lower() for x in projects}:
                return False
            if stablecoin_only and not p.get("stablecoin", False):
                return False
            return True
        return [p for p in pools if ok(p)]
