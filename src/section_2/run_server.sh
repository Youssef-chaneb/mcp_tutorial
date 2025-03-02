#!/bin/bash
# MCP Tutorial - Section 2: Run Server Script
# This script starts the weather MCP server.

# Ensure we're in the project root directory
cd "$(dirname "$0")/../.." || exit

# Activate the virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo "Starting Weather MCP Server..."
python src/section_2/weather_server.py
