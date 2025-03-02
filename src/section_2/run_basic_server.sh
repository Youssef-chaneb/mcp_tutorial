#!/bin/bash
# MCP Tutorial - Section 2: Run Basic Server
# This script runs the basic MCP server for the tutorial.

# Change to the project root directory
cd "$(dirname "$0")/../.."

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Virtual environment not found. Please create it first."
    exit 1
fi

# Run the basic server
echo "Starting Basic MCP Server..."
python src/section_2/basic_server.py
