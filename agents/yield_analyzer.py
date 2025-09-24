"""
DeFi Yield Analyzer Agent

This agent analyzes yield farming opportunities across various DeFi protocols.
It integrates with DefiLlama, CoinGecko, and other data sources to provide
comprehensive yield analysis.
"""

from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
from datetime import datetime, timedelta


class YieldAnalyzerAgent:
    """
    Agent responsible for analyzing DeFi yield opportunities.
    
    This agent:
    1. Fetches yield data from various protocols
    2. Calculates risk-adjusted returns
    3. Identifies the best opportunities
    4. Provides recommendations
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.defillama_base_url = "https://api.llama.fi"
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        
    async def analyze_yield_opportunities(
        self, 
        chains: List[str] = None,
        min_apy: float = 5.0,
        max_risk_score: float = 7.0
    ) -> Dict[str, Any]:
        """
        Analyze yield farming opportunities across specified chains.
        
        Args:
            chains: List of blockchain networks to analyze
            min_apy: Minimum APY threshold
            max_risk_score: Maximum risk score (1-10)
            
        Returns:
            Dictionary containing analyzed opportunities
        """
        if chains is None:
            chains = ["ethereum", "polygon", "arbitrum", "optimism"]
            
        opportunities = []
        
        for chain in chains:
            chain_opportunities = await self._get_chain_opportunities(
                chain, min_apy, max_risk_score
            )
            opportunities.extend(chain_opportunities)
            
        # Sort by risk-adjusted APY
        opportunities.sort(
            key=lambda x: x.get('risk_adjusted_apy', 0), 
            reverse=True
        )
        
        return {
            "total_opportunities": len(opportunities),
            "chains_analyzed": chains,
            "opportunities": opportunities[:20],  # Top 20
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    async def _get_chain_opportunities(
        self, 
        chain: str, 
        min_apy: float, 
        max_risk_score: float
    ) -> List[Dict[str, Any]]:
        """Get yield opportunities for a specific chain."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get TVL data from DefiLlama
                tvl_url = f"{self.defillama_base_url}/protocols"
                async with session.get(tvl_url) as response:
                    if response.status == 200:
                        protocols = await response.json()
                        return self._filter_opportunities(
                            protocols, chain, min_apy, max_risk_score
                        )
        except Exception as e:
            print(f"Error fetching data for {chain}: {e}")
            return []
    
    def _filter_opportunities(
        self, 
        protocols: List[Dict], 
        chain: str, 
        min_apy: float, 
        max_risk_score: float
    ) -> List[Dict[str, Any]]:
        """Filter and process yield opportunities."""
        opportunities = []
        
        for protocol in protocols:
            if protocol.get('chain') == chain:
                # Calculate risk score based on TVL and other factors
                tvl = protocol.get('tvl', 0)
                risk_score = self._calculate_risk_score(protocol)
                
                if risk_score <= max_risk_score:
                    opportunity = {
                        "protocol": protocol.get('name'),
                        "chain": chain,
                        "tvl": tvl,
                        "risk_score": risk_score,
                        "apy": protocol.get('apy', 0),
                        "risk_adjusted_apy": self._calculate_risk_adjusted_apy(
                            protocol.get('apy', 0), risk_score
                        )
                    }
                    opportunities.append(opportunity)
        
        return opportunities
    
    def _calculate_risk_score(self, protocol: Dict) -> float:
        """Calculate risk score for a protocol (1-10, lower is better)."""
        tvl = protocol.get('tvl', 0)
        
        # Base risk score
        risk_score = 5.0
        
        # Adjust based on TVL (higher TVL = lower risk)
        if tvl > 1000000000:  # > $1B TVL
            risk_score -= 2.0
        elif tvl > 100000000:  # > $100M TVL
            risk_score -= 1.0
        elif tvl < 10000000:  # < $10M TVL
            risk_score += 2.0
            
        # Adjust based on protocol age (if available)
        # This would need additional data from other sources
        
        return max(1.0, min(10.0, risk_score))
    
    def _calculate_risk_adjusted_apy(self, apy: float, risk_score: float) -> float:
        """Calculate risk-adjusted APY."""
        # Simple risk adjustment: higher risk = lower adjusted APY
        risk_multiplier = 1.0 - (risk_score - 1) * 0.1
        return apy * risk_multiplier


# Example usage
async def main():
    """Example usage of the Yield Analyzer Agent."""
    config = {
        "defillama_api_key": "",  # DefiLlama is free
        "coingecko_api_key": "your_key_here"
    }
    
    agent = YieldAnalyzerAgent(config)
    
    # Analyze opportunities
    results = await agent.analyze_yield_opportunities(
        chains=["ethereum", "polygon"],
        min_apy=5.0,
        max_risk_score=7.0
    )
    
    print(f"Found {results['total_opportunities']} opportunities")
    for opp in results['opportunities'][:5]:
        print(f"- {opp['protocol']}: {opp['apy']:.2f}% APY (Risk: {opp['risk_score']:.1f})")


if __name__ == "__main__":
    asyncio.run(main())
