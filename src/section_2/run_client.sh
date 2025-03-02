#!/bin/bash
# MCP Tutorial - Section 2: Run Client Script
# This script runs the client tests for the MCP server.

# Change to the project root directory
cd "$(dirname "$0")/../.."

# Check for virtual environment and activate it
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo "Running Weather MCP Client Tests..."
# Run the simple client and save output to a log file while still showing it on screen
python src/section_2/weather_client.py 2>&1 | tee weather_client_output.log 