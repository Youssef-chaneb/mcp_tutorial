#!/bin/bash
# MCP Tutorial - Section 2: Run Basic Client
# This script runs the basic MCP client for the tutorial.

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

# Run the basic client
echo "Running Basic MCP Client Tests..."
python src/section_2/simple_client.py 