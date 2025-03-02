#!/usr/bin/env python3
"""
MCP Tutorial - Section 1: Hello MCP Example
A simple example to demonstrate basic MCP concepts.
"""
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def simple_mcp_example():
    """
    A simple example that demonstrates connecting to an MCP server
    and using a basic tool.
    """
    print("="*50)
    print("MCP 'Hello World' Example")
    print("="*50)
    
    print("\n1. Setting up a sample MCP server connection...\n")
    
    # In a real application, you would specify the path to an actual server
    # For this example, we'll use a placeholder path
    server_script = "example_server.py"
    
    # Set up server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
        env=None
    )
    
    print(f"Server parameters configured for: {server_script}")
    print("In a real scenario, this would connect to a running MCP server.")
    print("You'll learn how to create a complete server in Section 2.")
    
    # Note: The code below would work with an actual server
    # This is commented out since we don't have a real server yet
    """
    # Connect to the server
    async with AsyncExitStack() as stack:
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await stack.enter_async_context(ClientSession(stdio, write))
        
        # Initialize the session
        await session.initialize()
        
        # List available tools
        response = await session.list_tools()
        tools = response.tools
        print(f"Available tools: {[tool.name for tool in tools]}")
        
        # Call a tool if available
        if any(tool.name == "echo" for tool in tools):
            result = await session.call_tool(
                "echo",
                {
                    "message": "Hello from MCP!"
                }
            )
            print(f"Response from echo tool: {result}")
    """
    
    print("\n2. MCP Client Structure:")
    print("   - Connection management (StdioServerParameters, stdio_client)")
    print("   - Session handling (ClientSession)")
    print("   - Tool discovery (list_tools)")
    print("   - Tool execution (call_tool)")
    
    print("\n3. In Section 2, you'll learn how to:")
    print("   - Create a real MCP server")
    print("   - Register tools for the server")
    print("   - Connect a client to your server")
    print("   - Execute tool calls through MCP")
    
    print("\n" + "="*50)
    print("Key MCP concepts demonstrated:")
    print("  - Server parameters configuration")
    print("  - Client-server communication flow")
    print("  - Session initialization")
    print("  - Tool discovery and invocation")
    print("="*50)

if __name__ == "__main__":
    # Run the example
    asyncio.run(simple_mcp_example()) 