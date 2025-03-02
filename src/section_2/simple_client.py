"""
MCP Tutorial - Section 2: Client-Server Fundamentals
This script demonstrates how to create a client that connects to an MCP server.
"""
import asyncio
import logging
import sys
import json
from contextlib import AsyncExitStack
from datetime import timedelta

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def test_server():
    """Test connecting to the MCP server and calling its tools."""
    logger.info("Starting client test...")
    
    # Create an AsyncExitStack to manage resources
    exit_stack = AsyncExitStack()
    
    try:
        # Set up the server parameters using StdioServerParameters
        server_script_path = "src/section_2/basic_server.py"
        server_params = StdioServerParameters(
            command=sys.executable,  # Use sys.executable for better portability
            args=[server_script_path],
            env=None
        )
        
        logger.info(f"Connecting to server at {server_script_path}...")
        
        # Connect to the server using stdio_client
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        read_stream, write_stream = stdio_transport
        
        # Create the client session with a reasonable timeout
        client = await exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream, read_timeout_seconds=timedelta(seconds=10))
        )
        
        # IMPORTANT: Initialize the session before making any tool calls
        logger.info("Initializing the client session...")
        await client.initialize()
        
        # List available tools
        response = await client.list_tools()
        tools = response.tools
        logger.info(f"Connected to server with tools: {[tool.name for tool in tools]}")
        
        # Helper function to safely extract content from responses
        def extract_content(response):
            """Extract content from a tool response, handling different formats."""
            if not response.content:
                logger.debug("No content in response")
                return None
                
            # If there's only one content item, process it normally
            if len(response.content) == 1:
                content = response.content[0].text
                logger.debug(f"Single content item: {content!r}")
                
                # Try to parse as JSON if it looks like JSON
                if content and (content.startswith('{') or content.startswith('[')):
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError as e:
                        logger.debug(f"JSON decode error: {e}")
                        # If it's not valid JSON, return the raw text
                        return content
                
                # Return raw text for non-JSON responses
                return content
            else:
                # If there are multiple content items, collect them into a list
                logger.debug(f"Multiple content items: {len(response.content)}")
                return [item.text for item in response.content]
        
        # 1. Test the echo tool
        logger.info("\n=== Testing echo tool ===")
        echo_text = "Hello, MCP World!"
        logger.info(f"Calling echo with: '{echo_text}'")
        
        echo_response = await client.call_tool("echo", {"text": echo_text})
        echo_result = extract_content(echo_response)
        
        logger.info(f"Echo result: {echo_result}")
        assert echo_result == echo_text, "Echo result didn't match input"
        logger.info("✅ Echo tool test passed!")
        
        # 2. Test the add_numbers tool
        logger.info("\n=== Testing add_numbers tool ===")
        a, b = 42.5, 7.5
        logger.info(f"Calling add_numbers with: {a} and {b}")
        
        add_response = await client.call_tool("add_numbers", {"a": a, "b": b})
        add_result = extract_content(add_response)
        
        logger.info(f"Add result: {add_result}")
        assert add_result["result"] == 50.0, "Addition result didn't match expected output"
        logger.info("✅ Add numbers tool test passed!")
        
        # 3. Test the sort_list tool
        logger.info("\n=== Testing sort_list tool ===")
        items = ["banana", "apple", "cherry", "date"]
        logger.info(f"Calling sort_list with: {items}")
        
        # Test normal sort
        sort_response = await client.call_tool("sort_list", {"items": items})
        
        # Log response details for debugging
        logger.info(f"Sort response content count: {len(sort_response.content) if sort_response.content else 0}")
        
        # Extract the content
        sort_result = extract_content(sort_response)
        logger.info(f"Sort result: {sort_result}")
        
        # For the sort_list tool, we expect a list of strings
        expected_result = sorted(items)
        assert sort_result == expected_result, f"Sort result didn't match expected output. Got {sort_result}, expected {expected_result}"
        logger.info("✅ Sort list tool test passed!")
        
        # Test reverse sort
        logger.info("Calling sort_list with reverse=True")
        reverse_sort_response = await client.call_tool(
            "sort_list", {"items": items, "reverse": True}
        )
        
        # Extract the content
        reverse_sort_result = extract_content(reverse_sort_response)
        logger.info(f"Reverse sort result: {reverse_sort_result}")
        
        # For the reverse sort, we expect a list of strings in reverse order
        expected_reverse_result = sorted(items, reverse=True)
        assert reverse_sort_result == expected_reverse_result, f"Reverse sort didn't match expected output. Got {reverse_sort_result}, expected {expected_reverse_result}"
        logger.info("✅ Reverse sort list tool test passed!")
        
        logger.info("\n=== All tool tests passed! ===")
    except asyncio.TimeoutError:
        logger.error("Tool call timed out")
        raise
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise
    finally:
        # Clean up resources using AsyncExitStack
        try:
            logger.info("Cleaning up resources...")
            await exit_stack.aclose()
            logger.info("Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error while cleaning up resources: {e}")

async def main():
    """Main function to run the client tests."""
    try:
        # Set a timeout for the entire test
        await asyncio.wait_for(test_server(), timeout=60.0)
        logger.info("Client test completed successfully!")
    except asyncio.TimeoutError:
        logger.error("Client test timed out after 60 seconds")
    except Exception as e:
        logger.exception(f"Error during client test: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 