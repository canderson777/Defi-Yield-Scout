"""
DeFi Risk Assessor Agent

This agent evaluates the risk profile of DeFi protocols and yield opportunities.
It analyzes smart contract security, TVL stability, protocol governance, and other risk factors.
"""

from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
from datetime import datetime, timedelta
from enum import Enum


class RiskLevel(Enum):
    """Risk level enumeration."""
    VERY_LOW = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    VERY_HIGH = 5


class RiskAssessorAgent:
    """
    Agent responsible for assessing risk in DeFi protocols.
    
    This agent:
    1. Analyzes smart contract security
    2. Evaluates TVL stability and trends
    3. Assesses protocol governance
    4. Calculates composite risk scores
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.defillama_base_url = "https://api.llama.fi"
        self.etherscan_base_url = "https://api.etherscan.io/api"
        
    async def assess_protocol_risk(
        self, 
        protocol_name: str,
        contract_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assess the risk profile of a DeFi protocol.
        
        Args:
            protocol_name: Name of the protocol
            contract_address: Optional contract address for detailed analysis
            
        Returns:
            Dictionary containing risk assessment
        """
        risk_factors = {}
        
        # TVL Risk Assessment
        tvl_risk = await self._assess_tvl_risk(protocol_name)
        risk_factors['tvl_risk'] = tvl_risk
        
        # Governance Risk Assessment
        governance_risk = await self._assess_governance_risk(protocol_name)
        risk_factors['governance_risk'] = governance_risk
        
        # Smart Contract Risk Assessment
        if contract_address:
            contract_risk = await self._assess_contract_risk(contract_address)
            risk_factors['contract_risk'] = contract_risk
        
        # Calculate composite risk score
        composite_risk = self._calculate_composite_risk(risk_factors)
        
        return {
            "protocol": protocol_name,
            "risk_level": self._get_risk_level(composite_risk),
            "composite_risk_score": composite_risk,
            "risk_factors": risk_factors,
            "assessment_timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_recommendations(composite_risk, risk_factors)
        }
    
    async def _assess_tvl_risk(self, protocol_name: str) -> Dict[str, Any]:
        """Assess TVL-related risks."""
        try:
            async with aiohttp.ClientSession() as session:
                # Get historical TVL data
                tvl_url = f"{self.defillama_base_url}/protocol/{protocol_name.lower().replace(' ', '-')}"
                async with session.get(tvl_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._analyze_tvl_trends(data)
        except Exception as e:
            print(f"Error assessing TVL risk for {protocol_name}: {e}")
            return {"risk_score": 5.0, "factors": ["Data unavailable"]}
    
    def _analyze_tvl_trends(self, tvl_data: Dict) -> Dict[str, Any]:
        """Analyze TVL trends for risk assessment."""
        # This is a simplified analysis
        # In practice, you'd analyze historical TVL data
        
        current_tvl = tvl_data.get('tvl', 0)
        
        risk_factors = []
        risk_score = 5.0  # Default medium risk
        
        # TVL size risk
        if current_tvl < 10000000:  # < $10M
            risk_score += 2.0
            risk_factors.append("Low TVL (< $10M)")
        elif current_tvl > 1000000000:  # > $1B
            risk_score -= 1.0
            risk_factors.append("High TVL (> $1B)")
        
        # TVL volatility (simplified)
        # In practice, you'd calculate actual volatility from historical data
        risk_factors.append("TVL volatility analysis needed")
        
        return {
            "risk_score": max(1.0, min(10.0, risk_score)),
            "current_tvl": current_tvl,
            "factors": risk_factors
        }
    
    async def _assess_governance_risk(self, protocol_name: str) -> Dict[str, Any]:
        """Assess governance-related risks."""
        # This is a simplified assessment
        # In practice, you'd analyze governance tokens, voting patterns, etc.
        
        risk_factors = []
        risk_score = 5.0  # Default medium risk
        
        # Check if protocol has governance token
        # This would require additional data sources
        risk_factors.append("Governance analysis needed")
        
        return {
            "risk_score": risk_score,
            "factors": risk_factors
        }
    
    async def _assess_contract_risk(self, contract_address: str) -> Dict[str, Any]:
        """Assess smart contract risks."""
        risk_factors = []
        risk_score = 5.0  # Default medium risk
        
        # Check if contract is verified on Etherscan
        try:
            async with aiohttp.ClientSession() as session:
                verify_url = f"{self.etherscan_base_url}?module=contract&action=getsourcecode&address={contract_address}&apikey={self.config.get('etherscan_api_key', '')}"
                async with session.get(verify_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result', [{}])[0].get('SourceCode'):
                            risk_score -= 1.0
                            risk_factors.append("Contract verified on Etherscan")
                        else:
                            risk_score += 2.0
                            risk_factors.append("Contract not verified")
        except Exception as e:
            risk_factors.append(f"Contract verification check failed: {e}")
        
        return {
            "risk_score": max(1.0, min(10.0, risk_score)),
            "factors": risk_factors
        }
    
    def _calculate_composite_risk(self, risk_factors: Dict[str, Any]) -> float:
        """Calculate composite risk score from all factors."""
        scores = []
        
        for factor_name, factor_data in risk_factors.items():
            if isinstance(factor_data, dict) and 'risk_score' in factor_data:
                scores.append(factor_data['risk_score'])
        
        if scores:
            return sum(scores) / len(scores)
        else:
            return 5.0  # Default medium risk
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert numeric risk score to risk level."""
        if risk_score <= 2.0:
            return RiskLevel.VERY_LOW.name
        elif risk_score <= 4.0:
            return RiskLevel.LOW.name
        elif risk_score <= 6.0:
            return RiskLevel.MEDIUM.name
        elif risk_score <= 8.0:
            return RiskLevel.HIGH.name
        else:
            return RiskLevel.VERY_HIGH.name
    
    def _generate_recommendations(
        self, 
        risk_score: float, 
        risk_factors: Dict[str, Any]
    ) -> List[str]:
        """Generate risk-based recommendations."""
        recommendations = []
        
        if risk_score > 7.0:
            recommendations.append("High risk - consider smaller position size")
            recommendations.append("Monitor protocol closely for changes")
        elif risk_score > 5.0:
            recommendations.append("Medium risk - standard due diligence recommended")
        else:
            recommendations.append("Lower risk - still monitor for changes")
        
        # Add specific recommendations based on risk factors
        for factor_name, factor_data in risk_factors.items():
            if isinstance(factor_data, dict) and 'factors' in factor_data:
                for factor in factor_data['factors']:
                    if "not verified" in factor.lower():
                        recommendations.append("Consider waiting for contract verification")
                    elif "low tvl" in factor.lower():
                        recommendations.append("Start with smaller position due to low TVL")
        
        return recommendations


# Example usage
async def main():
    """Example usage of the Risk Assessor Agent."""
    config = {
        "etherscan_api_key": "your_etherscan_key_here"
    }
    
    agent = RiskAssessorAgent(config)
    
    # Assess risk for a protocol
    risk_assessment = await agent.assess_protocol_risk(
        protocol_name="Uniswap V3",
        contract_address="0x1F98431c8aD98523631AE4a59f267346ea31F984"  # UNI token
    )
    
    print(f"Risk Level: {risk_assessment['risk_level']}")
    print(f"Risk Score: {risk_assessment['composite_risk_score']:.2f}")
    print("Recommendations:")
    for rec in risk_assessment['recommendations']:
        print(f"- {rec}")


if __name__ == "__main__":
    asyncio.run(main())
