"""
MCP Tutorial - Section 2: Weather Client
This script demonstrates how to create a client that connects to the weather MCP server.
"""
import asyncio
import logging
import sys
import os
import json
from datetime import timedelta
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def test_weather_server():
    """Test connecting to the MCP weather server and calling its tools."""
    logger.info("Starting weather client test...")
    
    # Create an AsyncExitStack to manage resources
    exit_stack = AsyncExitStack()
    
    try:
        # Set up the server parameters
        server_script_path = os.path.join("src", "section_2", "weather_server.py")
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[server_script_path],
            env=None
        )
        
        logger.info(f"Connecting to weather server at {server_script_path}...")
        
        # Connect to the server using stdio_client
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        read_stream, write_stream = stdio_transport
        
        # Create the client session
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
        
        # Helper function to extract JSON content from tool response
        def extract_json_content(response):
            # Get the first text content
            text_content = response.content[0].text
            # Parse the JSON string
            return json.loads(text_content)
        
        # 1. Test the weather forecast tool
        logger.info("\n=== Testing get_weather_forecast tool ===")
        
        # Test with valid parameters
        city = "New York"
        days = 3
        units = "celsius"
        logger.info(f"Getting weather forecast for {city} for {days} days in {units}")
        
        try:
            # Call the tool
            forecast_response = await client.call_tool(
                "get_weather_forecast", 
                {"city": city, "days": days, "units": units}
            )
            
            # Extract JSON content from response
            forecast_result = extract_json_content(forecast_response)
            logger.info(f"Weather forecast result: {forecast_result}")
            
            # Validate the response
            assert "city" in forecast_result, "Missing 'city' in forecast response"
            assert "forecast" in forecast_result, "Missing 'forecast' in forecast response"
            assert len(forecast_result["forecast"]) == days, f"Expected {days} days in forecast"
            
            logger.info("✅ Weather forecast tool test passed!")
            
            # Test with fahrenheit units
            logger.info("\nTesting forecast with fahrenheit units")
            fahrenheit_response = await client.call_tool(
                "get_weather_forecast", 
                {"city": city, "days": 1, "units": "fahrenheit"}
            )
            
            fahrenheit_result = extract_json_content(fahrenheit_response)
            logger.info(f"Fahrenheit forecast result: {fahrenheit_result}")
            assert fahrenheit_result["forecast"][0]["temperature_unit"] == "°F", "Temperature unit should be °F"
            
            logger.info("✅ Fahrenheit units test passed!")
            
            # Test with invalid city
            logger.info("\nTesting forecast with invalid city")
            invalid_city_response = await client.call_tool(
                "get_weather_forecast", 
                {"city": "InvalidCity", "days": 1}
            )
            
            invalid_city_result = extract_json_content(invalid_city_response)
            logger.info(f"Invalid city result: {invalid_city_result}")
            assert "error" in invalid_city_result, "Error message should be returned for invalid city"
            
            logger.info("✅ Invalid city error handling test passed!")
            
            # 2. Test the weather alerts tool
            logger.info("\n=== Testing get_weather_alerts tool ===")
            
            # Test with valid city
            city = "London"
            logger.info(f"Getting weather alerts for {city}")
            
            alerts_response = await client.call_tool(
                "get_weather_alerts", 
                {"city": city}
            )
            
            alerts_result = extract_json_content(alerts_response)
            logger.info(f"Weather alerts result: {alerts_result}")
            
            # Validate the response
            assert "city" in alerts_result, "Missing 'city' in alerts response"
            assert "alerts" in alerts_result, "Missing 'alerts' in alerts response"
            assert isinstance(alerts_result["alerts"], list), "Alerts should be a list"
            
            logger.info("✅ Weather alerts tool test passed!")
            
            # Test with invalid city
            logger.info("\nTesting alerts with invalid city")
            invalid_city_alerts_response = await client.call_tool(
                "get_weather_alerts", 
                {"city": "InvalidCity"}
            )
            
            invalid_city_alerts = extract_json_content(invalid_city_alerts_response)
            logger.info(f"Invalid city alerts result: {invalid_city_alerts}")
            assert "error" in invalid_city_alerts, "Error message should be returned for invalid city"
            
            logger.info("✅ Invalid city error handling for alerts test passed!")
            
            # 3. Try different cities
            logger.info("\n=== Testing weather tools with different cities ===")
            cities = ["Tokyo", "Cairo", "Sydney"]
            
            for test_city in cities:
                logger.info(f"\nTesting forecast for {test_city}")
                city_forecast_response = await client.call_tool(
                    "get_weather_forecast", 
                    {"city": test_city, "days": 1}
                )
                city_forecast = extract_json_content(city_forecast_response)
                logger.info(f"{test_city} forecast: {city_forecast}")
                
                logger.info(f"Testing alerts for {test_city}")
                city_alerts_response = await client.call_tool(
                    "get_weather_alerts", 
                    {"city": test_city}
                )
                city_alerts = extract_json_content(city_alerts_response)
                logger.info(f"{test_city} alerts: {city_alerts}")
            
            logger.info("\n=== All weather tool tests passed! ===")
            
        except asyncio.TimeoutError:
            logger.error("Tool call timed out")
            raise
        except Exception as e:
            logger.error(f"Error calling tool: {e}")
            raise
        
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise
    finally:
        # Clean up resources
        try:
            logger.info("Cleaning up resources...")
            await exit_stack.aclose()
            logger.info("Resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error while cleaning up resources: {e}")

async def main():
    """Main function to run the weather client tests."""
    try:
        # Set a timeout for the entire test
        await asyncio.wait_for(test_weather_server(), timeout=120.0)
        logger.info("Weather client test completed successfully!")
    except asyncio.TimeoutError:
        logger.error("Weather client test timed out after 120 seconds")
    except Exception as e:
        logger.exception(f"Error during weather client test: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 