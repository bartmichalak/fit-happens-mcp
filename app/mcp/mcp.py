from fastmcp import FastMCP

from app.mcp.tools import hello, workouts

mcp_router = FastMCP(name="Main MCP")

mcp_router.mount(hello.hello_router)
mcp_router.mount(workouts.workouts_router)