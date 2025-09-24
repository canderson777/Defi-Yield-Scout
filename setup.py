"""
DeFi Yield Scout Setup Script

This script helps set up the DeFi Yield Scout project on Windows.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True


def check_dependencies():
    """Check if required dependencies are available."""
    required_packages = [
        "aiohttp",
        "pandas", 
        "requests",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is not installed")
    
    return missing_packages


def install_dependencies(packages):
    """Install missing dependencies."""
    if not packages:
        print("✅ All dependencies are already installed")
        return True
    
    print(f"\nInstalling missing dependencies: {', '.join(packages)}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        try:
            # Copy env.example to .env
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API keys")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env.example file not found")
        return False


def create_directories():
    """Create necessary directories."""
    directories = [
        "data",
        "logs", 
        "results",
        "agents"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def test_configuration():
    """Test the configuration."""
    try:
        from config import load_config, print_config_status
        config = load_config()
        print_config_status(config)
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("DeFi Yield Scout Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check dependencies
    missing_packages = check_dependencies()
    if missing_packages:
        if not install_dependencies(missing_packages):
            return False
    
    # Create directories
    create_directories()
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Test configuration
    print("\nTesting configuration...")
    test_configuration()
    
    print("\n" + "=" * 50)
    print("✅ DeFi Yield Scout setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python config.py to verify configuration")
    print("3. Start developing your DeFi agents!")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
