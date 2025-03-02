"""
MCP Tutorial - Section 2: Client-Server Fundamentals
This script demonstrates how to set up a basic MCP server with simple tools.
"""
import asyncio
import logging
from typing import Dict, List, Union, Any

from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    """
    Start and run the basic MCP server.
    """
    logger.info("Starting MCP server...")
    
    # Initialize the MCP server with a name
    server = FastMCP("Basic MCP Server")
    
    # Register an echo tool
    @server.tool()
    async def echo(text: str) -> str:
        """
        Echo back the input text.
        
        Args:
            text: The text to echo back
            
        Returns:
            The same text that was provided
        """
        logger.info(f"Echoing: {text}")
        return text
    
    # Register an add_numbers tool
    @server.tool()
    async def add_numbers(a: float, b: float) -> Dict[str, float]:
        """
        Add two numbers together.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            A dictionary containing the result of the addition
        """
        logger.info(f"Adding numbers: {a} + {b}")
        result = a + b
        return {"result": result}
    
    # Register a sort_list tool
    @server.tool()
    async def sort_list(items: List[str], reverse: bool = False) -> List[str]:
        """
        Sort a list of strings.
        
        Args:
            items: The list of strings to sort
            reverse: Whether to sort in reverse order (default: False)
            
        Returns:
            The sorted list
        """
        logger.info(f"Sorting list: {items} (reverse={reverse})")
        return sorted(items, reverse=reverse)
    
    # Run the server using stdio
    logger.info("Server started. Running with stdio communication.")
    await server.run_stdio_async()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        logger.info("Server shutdown complete") 