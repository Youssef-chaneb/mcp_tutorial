"""
MCP Tutorial - Section 1: Environment Setup
This script checks if your environment is properly set up for the MCP tutorial.
"""
import sys
import importlib.util
import subprocess
import platform
import os

def check_python_version():
    """Check if Python version is 3.10 or higher."""
    required_version = (3, 10)
    current_version = sys.version_info[:2]
    
    if current_version >= required_version:
        print(f"✅ Python version: {sys.version.split()[0]} (required: 3.10+)")
        return True
    else:
        print(f"❌ Python version: {sys.version.split()[0]} (required: 3.10+)")
        return False

def check_package_installed(package_name):
    """Check if a package is installed."""
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package_name} is installed (version: {version})")
            return True
        except ImportError:
            print(f"❌ {package_name} is installed but failed to import")
            return False
    else:
        print(f"❌ {package_name} is not installed")
        return False

def check_mcp_package():
    """Check if the MCP package is installed and working."""
    try:
        # Try to import mcp (without needing __version__)
        import mcp
        
        try:
            from mcp import __version__
            print(f"✅ MCP package is installed (version: {__version__})")
        except ImportError:
            print(f"✅ MCP package is installed (version: unknown)")
        
        # Try importing key components
        try:
            from mcp.server.fastmcp import FastMCP
            print("✅ MCP server components are available")
        except ImportError as e:
            print(f"⚠️ MCP server components error: {e}")
        
        try:
            from mcp import ClientSession
            print("✅ MCP client components are available")
            return True
        except ImportError as e:
            print(f"❌ MCP client components error: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ MCP package error: {e}")
        return False

def check_os_compatibility():
    """Check OS compatibility."""
    system = platform.system()
    if system in ['Darwin', 'Linux', 'Windows']:
        print(f"✅ Operating System: {system} (supported)")
        return True
    else:
        print(f"⚠️ Operating System: {system} (may not be fully supported)")
        return False

def main():
    """Check environment setup for MCP tutorial."""
    print("==== MCP Tutorial Environment Check ====\n")
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check essential packages
    packages_ok = True
    essential_packages = ['asyncio', 'typing', 'pydantic', 'fastapi', 'aiohttp']
    for package in essential_packages:
        if not check_package_installed(package):
            packages_ok = False
    
    # Check MCP package
    mcp_ok = check_mcp_package()
    
    # Check OS compatibility
    os_ok = check_os_compatibility()
    
    print("\n===== Summary =====")
    if all([python_ok, packages_ok, mcp_ok, os_ok]):
        print("✅ Your environment is ready for the MCP tutorial!")
    else:
        print("⚠️ Please fix the issues above before continuing with the tutorial.")
        
        # Suggest how to fix missing packages
        if not packages_ok or not mcp_ok:
            print("\nYou can install missing packages with:")
            print("pip install -r requirements.txt")
    
    print("\nFor more information about MCP, visit: https://github.com/anthropics/anthropic-tools")

if __name__ == "__main__":
    main() 