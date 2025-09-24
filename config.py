"""
DeFi Yield Scout Configuration

This module contains configuration settings for the DeFi Yield Scout application.
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class DeFiYieldScoutConfig:
    """Configuration class for DeFi Yield Scout."""
    
    # API Keys
    litellm_api_key: str = ""
    coingecko_api_key: str = ""
    etherscan_api_key: str = ""
    alchemy_api_key: str = ""
    e2b_api_key: str = ""
    
    # AWS Configuration (optional)
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket_name: str = ""
    aws_region: str = "us-east-1"
    
    # DeFi Configuration
    default_chains: List[str] = None
    max_apy_threshold: float = 1000.0
    risk_tolerance: str = "medium"
    
    # Analysis Settings
    min_tvl_threshold: float = 1000000.0  # $1M minimum TVL
    max_risk_score: float = 7.0
    analysis_timeout: int = 30  # seconds
    
    def __post_init__(self):
        """Initialize configuration from environment variables."""
        if self.default_chains is None:
            self.default_chains = ["ethereum", "polygon", "arbitrum", "optimism"]
        
        # Load from environment variables
        self.litellm_api_key = os.getenv("LITELLM_API_KEY", self.litellm_api_key)
        self.coingecko_api_key = os.getenv("COINGECKO_API_KEY", self.coingecko_api_key)
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY", self.etherscan_api_key)
        self.alchemy_api_key = os.getenv("ALCHEMY_API_KEY", self.alchemy_api_key)
        self.e2b_api_key = os.getenv("E2B_API_KEY", self.e2b_api_key)
        
        # AWS Configuration
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", self.aws_access_key_id)
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", self.aws_secret_access_key)
        self.s3_bucket_name = os.getenv("S3_BUCKET_NAME", self.s3_bucket_name)
        self.aws_region = os.getenv("AWS_REGION", self.aws_region)
        
        # DeFi Configuration
        chains_env = os.getenv("DEFAULT_CHAINS", "")
        if chains_env:
            self.default_chains = [chain.strip() for chain in chains_env.split(",")]
        
        self.max_apy_threshold = float(os.getenv("MAX_APY_THRESHOLD", self.max_apy_threshold))
        self.risk_tolerance = os.getenv("RISK_TOLERANCE", self.risk_tolerance)
        self.min_tvl_threshold = float(os.getenv("MIN_TVL_THRESHOLD", self.min_tvl_threshold))
        self.max_risk_score = float(os.getenv("MAX_RISK_SCORE", self.max_risk_score))
        self.analysis_timeout = int(os.getenv("ANALYSIS_TIMEOUT", self.analysis_timeout))
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Check required API keys
        if not self.litellm_api_key or self.litellm_api_key == "your_llm_api_key_here":
            issues.append("LITELLM_API_KEY is required for ROMA framework")
        
        # Check optional but recommended keys
        if not self.coingecko_api_key or self.coingecko_api_key == "your_coingecko_api_key_here":
            issues.append("COINGECKO_API_KEY recommended for better data quality")
        
        # Validate risk tolerance
        if self.risk_tolerance not in ["low", "medium", "high"]:
            issues.append("RISK_TOLERANCE must be 'low', 'medium', or 'high'")
        
        # Validate APY threshold
        if self.max_apy_threshold <= 0 or self.max_apy_threshold > 10000:
            issues.append("MAX_APY_THRESHOLD should be between 0 and 10000")
        
        return issues
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "litellm_api_key": self.litellm_api_key[:10] + "..." if self.litellm_api_key else "",
            "coingecko_api_key": self.coingecko_api_key[:10] + "..." if self.coingecko_api_key else "",
            "etherscan_api_key": self.etherscan_api_key[:10] + "..." if self.etherscan_api_key else "",
            "alchemy_api_key": self.alchemy_api_key[:10] + "..." if self.alchemy_api_key else "",
            "e2b_api_key": self.e2b_api_key[:10] + "..." if self.e2b_api_key else "",
            "aws_access_key_id": self.aws_access_key_id[:10] + "..." if self.aws_access_key_id else "",
            "s3_bucket_name": self.s3_bucket_name,
            "aws_region": self.aws_region,
            "default_chains": self.default_chains,
            "max_apy_threshold": self.max_apy_threshold,
            "risk_tolerance": self.risk_tolerance,
            "min_tvl_threshold": self.min_tvl_threshold,
            "max_risk_score": self.max_risk_score,
            "analysis_timeout": self.analysis_timeout
        }


def load_config() -> DeFiYieldScoutConfig:
    """Load configuration from environment variables."""
    return DeFiYieldScoutConfig()


def print_config_status(config: DeFiYieldScoutConfig) -> None:
    """Print configuration status."""
    print("DeFi Yield Scout Configuration Status:")
    print("=" * 50)
    
    # Check required configurations
    required_checks = [
        ("LiteLLM API Key", config.litellm_api_key and config.litellm_api_key != "your_llm_api_key_here"),
        ("CoinGecko API Key", config.coingecko_api_key and config.coingecko_api_key != "your_coingecko_api_key_here"),
        ("Etherscan API Key", config.etherscan_api_key and config.etherscan_api_key != "your_etherscan_api_key_here"),
    ]
    
    for name, status in required_checks:
        status_str = "✅ Configured" if status else "❌ Not configured"
        print(f"{name}: {status_str}")
    
    # Check optional configurations
    optional_checks = [
        ("E2B API Key", config.e2b_api_key and config.e2b_api_key != "your_e2b_api_key_here"),
        ("AWS S3", config.s3_bucket_name and config.s3_bucket_name != "your-s3-bucket-name"),
    ]
    
    print("\nOptional Features:")
    for name, status in optional_checks:
        status_str = "✅ Configured" if status else "⚠️  Not configured"
        print(f"{name}: {status_str}")
    
    # Print configuration issues
    issues = config.validate()
    if issues:
        print("\nConfiguration Issues:")
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("\n✅ Configuration is valid!")


if __name__ == "__main__":
    # Load and display configuration
    config = load_config()
    print_config_status(config)
