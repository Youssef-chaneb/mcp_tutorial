# MCP Tutorial

This project is a step-by-step tutorial for learning the Model Context Protocol (MCP), a framework that enables AI models to interact with external tools and resources.

## Tutorial Sections

1. **Introduction**
   - What is MCP and why it matters
   - MCP architecture and implementation
   - Getting started with the tutorial

2. **[Client-Server Fundamentals](src/section_2/README.md)**
   - Setting up a basic MCP server with simple tools
   - Creating a client that connects to the server
   - Understanding the client-server communication flow
   - Testing tool interactions with echo, add_numbers, and sort_list
   - Implementing a weather service with forecast and alerts tools

3. **Exploring Built-in Tools**
   - Using MCP's built-in tools
   - Understanding tool schemas and capabilities
   - Testing built-in tools with your client

4. **Loading Existing Tools**
   - Integrating community tools
   - Customizing existing tools
   - Extending tool functionality

5. **Creating Custom Tools**
   - Designing tool schemas
   - Implementing different tool types
   - Testing and debugging tools

6. **Advanced Client Configurations**
   - Creating specialized clients
   - Advanced connection methods
   - Error handling and retries
   - Client-side validation

7. **Resource Provisioning**
   - Understanding resource types
   - Resource registration and configuration
   - Resource management best practices

8. **Advanced Communication Patterns**
   - MCP message formats in detail
   - Advanced interaction patterns
   - Protocol debugging techniques
   - Performance optimization

9. **Real-life Examples with Agents**
   - Practical MCP applications
   - End-to-end workflows
   - Agent integration strategies

10. **Resources and References**
    - Additional learning resources
    - MCP ecosystem and community
    - Further exploration guides

11. **Capstone Project: Smart Research Assistant**
    - Building a complete web application
    - Integrating all learned concepts
    - Implementing practical AI tools

## Getting Started

1. Activate the virtual environment:
   ```
   source .venv/bin/activate
   ```

2. Navigate to the section you're interested in:
   ```
   cd src/section_X
   ```

3. Follow the README instructions in each section directory.

## Project Configuration

This project uses modern Python tooling:

- **Python 3.10+** is required
- **pyproject.toml** for dependency management
- **uv** for faster, more reliable package installation

To set up the project with uv:

```bash
# Install uv if you don't have it
pip install uv

# Create and activate a virtual environment
uv venv

# Install dependencies
uv pip install -e .

# Install development dependencies (optional)
uv pip install -e ".[dev]"
```

## Requirements

- Python 3.10+
- Dependencies are listed in pyproject.toml

## License

MIT