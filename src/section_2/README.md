# MCP Tutorial - Section 2: Client-Server Fundamentals

This section demonstrates the fundamental concepts of the Model Context Protocol (MCP) client-server architecture. You'll learn how to set up a basic MCP server with simple tools, create a client that connects to the server, and test tool interactions.

## Core Concepts

### 1. MCP Server

An MCP server exposes tools that clients can discover and call. Each tool has a defined schema and implementation.

**Key Components:**
- Server initialization with `FastMCP`
- Tool registration with the `@server.tool()` decorator
- Tool implementation with typed parameters and return values
- Server execution with `run_stdio_async()`

**Example from `basic_server.py`:**

```python
# Initialize the MCP server
server = FastMCP("Basic MCP Server")

# Register a tool with the server
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

# Run the server using stdio
await server.run_stdio_async()
```

### 2. MCP Client

An MCP client connects to a server, discovers available tools, and makes tool calls.

**Key Components:**
- Server connection with `stdio_client` and `StdioServerParameters`
- Client session creation with `ClientSession`
- Session initialization with `client.initialize()`
- Tool discovery with `client.list_tools()`
- Tool calls with `client.call_tool()`
- Response processing

**Example from `simple_client.py`:**

```python
# Set up the server parameters
server_params = StdioServerParameters(
    command=sys.executable,
    args=[server_script_path],
    env=None
)

# Connect to the server
stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
read_stream, write_stream = stdio_transport

# Create the client session
client = await exit_stack.enter_async_context(
    ClientSession(read_stream, write_stream, read_timeout_seconds=timedelta(seconds=10))
)

# Initialize the session before making any tool calls
await client.initialize()

# List available tools
response = await client.list_tools()
tools = response.tools
logger.info(f"Connected to server with tools: {[tool.name for tool in tools]}")

# Call a tool
echo_response = await client.call_tool("echo", {"text": "Hello, MCP World!"})
```

### 3. Response Handling

MCP tool responses contain content objects that need to be properly extracted and processed.

**Example from `simple_client.py`:**

```python
# Helper function to safely extract content from responses
def extract_content(response):
    """Extract content from a tool response, handling different formats."""
    if not response.content:
        return None
        
    # If there's only one content item, process it normally
    if len(response.content) == 1:
        content = response.content[0].text
        
        # Try to parse as JSON if it looks like JSON
        if content and (content.startswith('{') or content.startswith('[')):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If it's not valid JSON, return the raw text
                return content
        
        # Return raw text for non-JSON responses
        return content
    else:
        # If there are multiple content items, collect them into a list
        return [item.text for item in response.content]
```

### 4. Resource Management

Proper resource management is essential for MCP clients to ensure connections are properly closed.

**Example from `simple_client.py`:**

```python
# Create an AsyncExitStack to manage resources
exit_stack = AsyncExitStack()

try:
    # Use the exit stack to manage resources
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    client = await exit_stack.enter_async_context(ClientSession(...))
    
    # Use the client...
    
finally:
    # Clean up resources
    await exit_stack.aclose()
```

## Available Tools

### Basic Server Tools

1. **echo** - Echoes back the input text
   - Parameter: `text` (string)
   - Returns: The same text

2. **add_numbers** - Adds two numbers together
   - Parameters: `a` (float), `b` (float)
   - Returns: A dictionary with the result: `{"result": sum}`

3. **sort_list** - Sorts a list of strings
   - Parameters: `items` (list of strings), `reverse` (boolean, optional)
   - Returns: The sorted list

### Weather Server Tools

1. **get_weather_forecast** - Gets a weather forecast for a city
   - Parameters: `city` (string), `days` (integer, optional), `units` (string, optional)
   - Returns: A dictionary with the forecast data

2. **get_weather_alerts** - Gets weather alerts for a city
   - Parameter: `city` (string)
   - Returns: A dictionary with the alerts data

## Running the Examples

### Prerequisites

Make sure you have activated the virtual environment:

```bash
source .venv/bin/activate
```

### Basic Server and Client

1. **Start the Basic Server:**

```bash
./src/section_2/run_basic_server.sh
```

This will start the basic MCP server with the echo, add_numbers, and sort_list tools.

2. **In a new terminal, run the Basic Client:**

```bash
./src/section_2/run_basic_client.sh
```

The client will connect to the server, discover the available tools, and test each one.

### Weather Server and Client

1. **Start the Weather Server:**

```bash
./src/section_2/run_server.sh
```

This will start the weather MCP server with the get_weather_forecast and get_weather_alerts tools.

2. **In a new terminal, run the Weather Client:**

```bash
./src/section_2/run_client.sh
```

The client will connect to the server, discover the available tools, and test various weather scenarios.

## Key Takeaways

1. **Server-Client Architecture**: MCP follows a client-server architecture where the server exposes tools and the client calls them.

2. **Tool Registration**: Tools are registered with the server using decorators and include type annotations for parameters and return values.

3. **Session Initialization**: Always initialize the client session before making tool calls.

4. **Response Processing**: Tool responses contain content objects that need to be properly extracted and processed.

5. **Resource Management**: Use `AsyncExitStack` to properly manage resources and ensure connections are closed.

6. **Error Handling**: Implement proper error handling for tool calls and response processing.

## Next Steps

After completing this section, you should have a good understanding of the MCP client-server architecture and be ready to explore more advanced topics in the next sections.

- Section 3: Exploring Built-in Tools
- Section 4: Loading Existing Tools
- Section 5: Creating Custom Tools 