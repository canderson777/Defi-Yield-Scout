from __future__ import annotations
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from sentientresearchagent.tools.defillama import DefiLlamaClient
from sentientresearchagent.tools.coingecko import CoinGeckoClient
from sentientresearchagent.utils.risk import risk_score_pool

class YieldQuery(BaseModel):
    chains: List[str] = Field(default_factory=lambda: ["ethereum","base","arbitrum"])
    stablecoin_only: bool = False
    min_tvl_usd: float = 1_000_000
    max_pools: int = 25
    include_projects: Optional[List[str]] = None
    symbols: Optional[List[str]] = None

class PoolReport(BaseModel):
    project: str
    pool: str
    chain: str
    symbol: str
    apy: float
    tvl_usd: float
    base_apy: Optional[float] = None
    reward_apy: Optional[float] = None
    risk: Dict[str, Any]
    price_usd: Optional[float] = None
    url: Optional[str] = None

class ScoutResult(BaseModel):
    input: YieldQuery
    pools: List[PoolReport]
    notes: str

class DeFiYieldScout:
    def __init__(self):
        self.llama = DefiLlamaClient()
        self.cg = CoinGeckoClient()

    async def _enrich_pool(self, p: Dict[str,Any]) -> PoolReport:
        # Basic fields from DefiLlama yields API
        symbol = p.get("symbol")
        chain = p.get("chain")
        project = p.get("project")
        apy = float(p.get("apy") or 0.0)
        tvl = float(p.get("tvlUsd") or 0.0)
        base_apy = p.get("apyBase")
        reward_apy = p.get("apyReward")
        # Optional token price via CoinGecko (best-effort)
        price = None
        if p.get("underlyingTokens"):
            price = await self.cg.price_by_token(chain, p["underlyingTokens"][0])

        risk = risk_score_pool(p)
        return PoolReport(
            project=project, pool=p.get("pool"), chain=chain, symbol=symbol,
            apy=apy, tvl_usd=tvl, base_apy=base_apy, reward_apy=reward_apy,
            risk=risk, price_usd=price, url=p.get("url")
        )

    async def run(self, q: YieldQuery) -> ScoutResult:
        pools = await self.llama.fetch_pools(
            chains=q.chains,
            projects=q.include_projects,
            stablecoin_only=q.stablecoin_only
        )
        # Client-side filters
        filtered = [
            p for p in pools
            if (p.get("tvlUsd") or 0) >= q.min_tvl_usd
               and (not q.symbols or (p.get("symbol") or "").upper() in {s.upper() for s in q.symbols})
        ]
        # Rank by simple risk-adjusted APY (apy * log10(tvl+1) / (1+risk))
        def score(p):
            apy = float(p.get("apy") or 0)
            tvl = float(p.get("tvlUsd") or 0)
            base = risk_score_pool(p)
            r = base.get("total", 1.0)  # avoid divide by zero
            import math
            return apy * (math.log10(tvl+1)) / (1.0 + r)

        top = sorted(filtered, key=score, reverse=True)[: q.max_pools]
        reports = await asyncio.gather(*[self._enrich_pool(p) for p in top])

        return ScoutResult(
            input=q,
            pools=reports,
            notes="Source: DefiLlama Yields. Prices (best-effort) via CoinGecko."
        )
