"""
MCP Tutorial - Section 2: Weather Server
This script demonstrates how to set up an MCP server with weather forecast and alert tools.
"""
import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Define weather conditions
WEATHER_CONDITIONS = [
    "sunny", "partly cloudy", "cloudy", "rainy", "thunderstorm", 
    "snowy", "foggy", "windy", "hail"
]

# Define cities with base temperatures
CITIES = {
    "New York": {"base_temp_c": 15, "precipitation_chance": 30},
    "London": {"base_temp_c": 12, "precipitation_chance": 60},
    "Tokyo": {"base_temp_c": 20, "precipitation_chance": 40},
    "Sydney": {"base_temp_c": 25, "precipitation_chance": 20},
    "Paris": {"base_temp_c": 18, "precipitation_chance": 35},
    "Cairo": {"base_temp_c": 30, "precipitation_chance": 5},
    "Moscow": {"base_temp_c": 5, "precipitation_chance": 25},
    "Rio de Janeiro": {"base_temp_c": 27, "precipitation_chance": 15},
}

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def get_weather_condition(precipitation_chance: int) -> str:
    """Get a weather condition based on precipitation chance."""
    if precipitation_chance < 10:
        return random.choice(["sunny", "sunny", "sunny", "partly cloudy"])
    elif precipitation_chance < 30:
        return random.choice(["partly cloudy", "partly cloudy", "cloudy"])
    elif precipitation_chance < 50:
        return random.choice(["cloudy", "cloudy", "rainy"])
    elif precipitation_chance < 70:
        return random.choice(["rainy", "rainy", "thunderstorm"])
    else:
        return random.choice(["rainy", "thunderstorm", "thunderstorm"])

async def main():
    """
    Start and run the weather MCP server.
    """
    logger.info("Starting Weather MCP Server...")
    
    # Initialize the MCP server with a name
    server = FastMCP("Weather MCP Server")
    
    # Register a weather forecast tool
    @server.tool()
    async def get_weather_forecast(city: str, days: int = 3, units: str = "celsius") -> Dict[str, Union[str, List[Dict[str, Union[str, float]]]]]:
        """
        Get a weather forecast for a specified city and number of days.
        
        Args:
            city: The name of the city to get the forecast for
            days: The number of days to forecast (default: 3)
            units: Temperature units, either 'celsius' or 'fahrenheit' (default: celsius)
            
        Returns:
            A dictionary containing the city name and a list of daily forecasts
        """
        logger.info(f"Generating weather forecast for {city} for {days} days in {units}")
        
        # Validate input
        if city not in CITIES:
            available_cities = ", ".join(CITIES.keys())
            return {
                "error": f"City '{city}' not found. Available cities: {available_cities}"
            }
        
        if days < 1 or days > 10:
            return {
                "error": "Days must be between 1 and 10"
            }
        
        if units not in ["celsius", "fahrenheit"]:
            return {
                "error": "Units must be either 'celsius' or 'fahrenheit'"
            }
        
        # Generate forecasts
        city_data = CITIES[city]
        base_temp_c = city_data["base_temp_c"]
        precipitation_chance = city_data["precipitation_chance"]
        
        forecasts = []
        for day_offset in range(days):
            date = datetime.now() + timedelta(days=day_offset)
            date_str = date.strftime("%Y-%m-%d")
            
            # Add some randomness to temperature
            temp_variation = random.uniform(-5, 5)
            temp_c = base_temp_c + temp_variation
            
            # Convert temperature if needed
            if units == "fahrenheit":
                temp = celsius_to_fahrenheit(temp_c)
                temp_unit = "°F"
            else:
                temp = temp_c
                temp_unit = "°C"
            
            # Vary precipitation chance slightly
            day_precipitation = max(0, min(100, precipitation_chance + random.randint(-10, 10)))
            
            # Get weather condition
            condition = get_weather_condition(day_precipitation)
            
            forecasts.append({
                "date": date_str,
                "condition": condition,
                "temperature": round(temp, 1),
                "temperature_unit": temp_unit,
                "precipitation_chance": day_precipitation
            })
        
        return {
            "city": city,
            "forecast": forecasts
        }
    
    # Register a weather alert tool
    @server.tool()
    async def get_weather_alerts(city: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Get current weather alerts for a specified city.
        
        Args:
            city: The name of the city to get alerts for
            
        Returns:
            A dictionary containing the city name and a list of weather alerts
        """
        logger.info(f"Checking weather alerts for {city}")
        
        # Validate input
        if city not in CITIES:
            available_cities = ", ".join(CITIES.keys())
            return {
                "error": f"City '{city}' not found. Available cities: {available_cities}"
            }
        
        # Generate alerts based on precipitation chance
        city_data = CITIES[city]
        precipitation_chance = city_data["precipitation_chance"]
        
        alerts = []
        
        # Generate random severe weather alerts
        if precipitation_chance > 60:
            alerts.append({
                "severity": "high",
                "type": "flood",
                "message": f"Flood warning in effect for {city} and surrounding areas"
            })
        elif precipitation_chance > 40:
            alerts.append({
                "severity": "medium",
                "type": "rain",
                "message": f"Heavy rain expected in {city} today"
            })
        
        # Add a heat alert for very hot cities
        if city_data["base_temp_c"] > 28:
            alerts.append({
                "severity": "medium",
                "type": "heat",
                "message": f"Heat advisory in effect for {city}"
            })
        
        # Add a cold alert for very cold cities
        if city_data["base_temp_c"] < 8:
            alerts.append({
                "severity": "medium",
                "type": "cold",
                "message": f"Cold weather advisory in effect for {city}"
            })
        
        # Sometimes return no alerts
        if random.random() > 0.7:
            alerts = []
        
        return {
            "city": city,
            "alerts": alerts
        }
    
    # Run the server using stdio
    logger.info("Weather Server started. Running with stdio communication.")
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