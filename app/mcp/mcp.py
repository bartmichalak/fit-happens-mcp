from fastmcp import FastMCP

from app.mcp.tools import hello, workouts, heart_rate

mcp_router = FastMCP(name="Main MCP")

mcp_router.mount(hello.hello_router)
mcp_router.mount(workouts.workouts_router)
mcp_router.mount(heart_rate.heart_rate_router)