"""
DeFi Yield Scout Example

This example demonstrates how to use the DeFi Yield Scout agents
to analyze yield farming opportunities.
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from config import load_config, print_config_status
from agents.yield_analyzer import YieldAnalyzerAgent
from agents.risk_assessor import RiskAssessorAgent


async def analyze_yield_opportunities():
    """Example: Analyze yield opportunities across multiple chains."""
    print("🔍 Analyzing DeFi Yield Opportunities")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Initialize yield analyzer
    yield_agent = YieldAnalyzerAgent(config.to_dict())
    
    # Analyze opportunities
    results = await yield_agent.analyze_yield_opportunities(
        chains=["ethereum", "polygon"],
        min_apy=5.0,
        max_risk_score=7.0
    )
    
    print(f"📊 Found {results['total_opportunities']} opportunities")
    print(f"🌐 Chains analyzed: {', '.join(results['chains_analyzed'])}")
    print(f"⏰ Analysis time: {results['analysis_timestamp']}")
    
    print("\n🏆 Top 5 Opportunities:")
    for i, opp in enumerate(results['opportunities'][:5], 1):
        print(f"{i}. {opp['protocol']} ({opp['chain']})")
        print(f"   APY: {opp['apy']:.2f}% | Risk: {opp['risk_score']:.1f} | TVL: ${opp['tvl']:,.0f}")
        print(f"   Risk-Adjusted APY: {opp['risk_adjusted_apy']:.2f}%")
        print()
    
    return results


async def assess_protocol_risk():
    """Example: Assess risk for a specific protocol."""
    print("🛡️  Assessing Protocol Risk")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Initialize risk assessor
    risk_agent = RiskAssessorAgent(config.to_dict())
    
    # Assess risk for a protocol
    risk_assessment = await risk_agent.assess_protocol_risk(
        protocol_name="Uniswap V3"
    )
    
    print(f"📋 Protocol: {risk_assessment['protocol']}")
    print(f"🎯 Risk Level: {risk_assessment['risk_level']}")
    print(f"📊 Risk Score: {risk_assessment['composite_risk_score']:.2f}/10")
    
    print("\n🔍 Risk Factors:")
    for factor_name, factor_data in risk_assessment['risk_factors'].items():
        if isinstance(factor_data, dict):
            print(f"  {factor_name}: {factor_data.get('risk_score', 'N/A')}/10")
            if 'factors' in factor_data:
                for factor in factor_data['factors']:
                    print(f"    - {factor}")
    
    print("\n💡 Recommendations:")
    for rec in risk_assessment['recommendations']:
        print(f"  • {rec}")
    
    return risk_assessment


async def main():
    """Main example function."""
    print("DeFi Yield Scout - Example Usage")
    print("=" * 40)
    
    # Check configuration
    config = load_config()
    print_config_status(config)
    
    # Check for configuration issues
    issues = config.validate()
    if issues:
        print("\n⚠️  Configuration issues detected:")
        for issue in issues:
            print(f"  • {issue}")
        print("\nPlease update your .env file with the required API keys.")
        return
    
    print("\n" + "=" * 50)
    
    try:
        # Example 1: Analyze yield opportunities
        yield_results = await analyze_yield_opportunities()
        
        print("\n" + "=" * 50)
        
        # Example 2: Assess protocol risk
        risk_results = await assess_protocol_risk()
        
        print("\n" + "=" * 50)
        print("✅ Example completed successfully!")
        print("\nNext steps:")
        print("1. Integrate with ROMA framework for advanced AI capabilities")
        print("2. Add more data sources and analysis methods")
        print("3. Build a web interface for user interaction")
        print("4. Deploy to production for real-world use")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("This is expected if API keys are not configured.")
        print("Please set up your .env file with valid API keys.")


if __name__ == "__main__":
    asyncio.run(main())
