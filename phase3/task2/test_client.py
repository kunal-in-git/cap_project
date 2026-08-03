"""Standalone MCP protocol test: spawns mcp_server.py as a subprocess
over stdio (the real transport) and calls both tools through an
actual mcp.ClientSession, not just as plain Python functions.
"""

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])


async def main() -> None:
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Tools exposed:", [t.name for t in tools.tools])

            result = await session.call_tool("search_books", {"query": "Orwell"})
            print("\nsearch_books('Orwell') ->")
            print(result.content[0].text)

            result = await session.call_tool("library_summary", {})
            print("\nlibrary_summary() ->")
            print(json.dumps(json.loads(result.content[0].text), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
