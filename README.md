# MCP Server

This project provides a Model Context Protocol (MCP) server built with FastMCP, enabling seamless integration with AI assistants and language models.

## Overview

MCP (Model Context Protocol) is a standard for connecting AI assistants to external data sources and tools. This server implements MCP using FastMCP, a Python framework that simplifies MCP server development.

## Features

- **FastMCP Integration**: Built on FastMCP for easy tool and resource management
- **Modular Architecture**: Organized tool structure with separate modules
- **Type Safety**: Full Pydantic integration for robust data validation
- **Easy Extension**: Simple pattern for adding new tools and capabilities
- **Workouts API Integration**: Access to external fitness data with comprehensive filtering and pagination

## Project Structure

```
app/mcp/
├── __init__.py
├── mcp.py              # Main MCP router configuration
└── tools/
    ├── __init__.py
    ├── hello.py        # Example tool implementation
    └── workouts.py     # Workouts API integration tool
```

## Getting Started

### Installation

```bash
# Install dependencies
uv sync
```

### Running the Server

```bash
# stdio transport
uv run fastmcp run app/main.py

# http transport
uv run fastmcp run app/main.py --transport http --port 8888
# choose any free port, default is 8000
```

### Adding New Tools

1. Create a new tool module in `app/mcp/tools/`
2. Define your tool using FastMCP decorators and add descriptive docstrings
3. Mount the tool router in `app/mcp/mcp.py`

Example tool implementation:

```python
from fastmcp import FastMCP

tool_router = FastMCP(name="My Tool")

@tool_router.tool
def my_tool(param: str) -> str:
    """Description of what this tool does."""
    return f"Result: {param}"
```

## Available Tools

### Workouts Tool

The `get_workouts` tool provides access to fitness data from an external API with comprehensive filtering, sorting, and pagination capabilities.

#### Parameters

- **Date Range**:
  - `start_date`: ISO 8601 format (e.g., '2023-12-01T00:00:00Z')
  - `end_date`: ISO 8601 format (e.g., '2023-12-31T23:59:59Z')

- **Workout Filters**:
  - `workout_type`: e.g., 'Outdoor Walk', 'Indoor Walk'
  - `location`: 'Indoor' or 'Outdoor'
  - `min_duration`: minimum duration in seconds
  - `max_duration`: maximum duration in seconds
  - `min_distance`: minimum distance in km
  - `max_distance`: maximum distance in km

- **Sorting & Pagination**:
  - `sort_by`: sort field (default: 'date')
  - `sort_order`: 'asc' or 'desc' (default: 'desc')
  - `limit`: number of results (1-100, default: 20)
  - `offset`: number of results to skip (default: 0)

#### Response Format

The tool returns a structured response containing:
- `data`: Array of workout objects with detailed metrics
- `meta`: Metadata including result count, date range, and filters

#### Example Usage

```python
# Get all workouts
workouts = get_workouts()

# Get workouts for a specific date range
workouts = get_workouts(
    start_date="2023-12-01T00:00:00Z",
    end_date="2023-12-31T23:59:59Z",
    limit=10
)

# Get outdoor workouts longer than 30 minutes
workouts = get_workouts(
    location="Outdoor",
    min_duration=1800,
    limit=5
)
```

## Configuration

The server uses Pydantic settings for configuration. Key settings can be configured through environment variables or a `.env` file.

### External API Configuration

Configure the external workouts API endpoint:

```bash
# .env file
EXTERNAL_API_BASE_URL=https://your-api-endpoint.com
EXTERNAL_API_TIMEOUT=30
```

## Dependencies

- **FastMCP**: Core MCP framework
- **Pydantic**: Data validation and settings management
- **httpx**: HTTP client for external API communication

## Integration

This MCP server can be integrated with various AI assistants and language models that support the MCP protocol, providing them with access to your custom tools and data sources. **We suggest to use HTTP transport for AI agents integrations**.
