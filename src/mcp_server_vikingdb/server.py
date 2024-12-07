from typing import Optional

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

import click
import mcp.types as types
import asyncio
import mcp

from .vikingdb import VikingDBConnector


def serve(
    vikingdb_host: str, 
    vikingdb_region: str, 
    vikingdb_ak: str, 
    vikingdb_sk: str,
    collection_name: str,
    index_name: str
) -> Server:
    """
    Encapsulates the connection to a VikingDB server and some  methods to interact with it.
    :param vikingdb_host: The host to use for the VikingDB server.
    :param vikingdb_region: The region to use for the VikingDB server.
    :param vikingdb_ak: The Access Key to use for the VikingDB server.
    :param vikingdb_sk: The Secret Key to use for the VikingDB server.
    :param collection_name: The name of the collection to use.
    :param index_name: The name of the index to use.
    """
    


    server = Server("mcp-server-vikingdb")

    vikingdb = VikingDBConnector(
            vikingdb_host,
            vikingdb_region,
            vikingdb_ak,
            vikingdb_sk,
            collection_name,
            index_name
        )
    
    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """
        List available tools.
        Each tool specifies its arguments using JSON Schema validation.
        """
        return [
            types.Tool(
                name="vikingdb-collection-intro",
                description="introduce the collection of vikingdb",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="vikingdb-index-intro",
                description="introduce the index of vikingdb",
                inputSchema={
                    "type": "object",
                 "properties": {},
                },
            ),
            types.Tool(
                name="vikingdb-upsert-information",
                description="upsert information to vikingdb for later use",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "information": {
                            "type": "string",
                        },
                    },
                    "required": ["information"],
                },
            ),
            types.Tool(
                name="vikingdb-search-information",
                description=(
                    "Look up information in VikingDB. Use this tool when you need to: \n"
                    " - Search for information by their query \n"
                    " - Access information for further analysis \n"
                    " - Get some personal information about the user"
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search for in the vikingdb",
                        },
                    },
                    "required": ["query"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """
        Handle tool execution requests.
        Tools can modify server state and notify clients of changes.
        """
        if name not in ["vikingdb-collection-intro","vikingdb-index-intro","vikingdb-upsert-information", "vikingdb-search-information"]:
            raise ValueError(f"Unknown tool: {name}")

        if name == "vikingdb-collection-intro":
            results = await vikingdb.collection_intro()
            return [types.TextContent(type="text", text=f"The basic information of Collection {collection_name} is {results}")]
        
        if name == "vikingdb-index-intro":
            results = await vikingdb.index_intro()
            return [types.TextContent(type="text", text=f"The basic information of Index {index_name} is {results}")]
        
        if name == "vikingdb-upsert-information":
            if not arguments or "information" not in arguments:
                raise ValueError("Missing required argument 'information'")
            information = arguments["information"]
            await vikingdb.upsert_information(information)
            return [types.TextContent(type="text", text=f"{information} has been added to vikingdb {collection_name}")]
        
        if name == "vikingdb-search-information":
            if not arguments or "query" not in arguments:
                raise ValueError("Missing required argument 'query'")
            query = arguments["query"]
            results = await vikingdb.search_information(query)
            return [types.TextContent(type="text", text=f"Search results for {query}:\n{results}")]
        
    return server
    
    
@click.command()
@click.option(
    "--vikingdb-host",
    envvar="VIKINGDB_HOST",
    required=True,
    help="VIKINGDB_HOST",
    default="api-vikingdb.volces.com",
)

@click.option(
    "--vikingdb-region",
    envvar="VIKINGDB_REGION",
    required=True,
    help="VIKINGDB_REGION",
)
@click.option(
    "--vikingdb-ak",
    envvar="VIKINGDB_AK",
    required=True,
    help="VIKINGDB_AK",
)
@click.option(
    "--vikingdb-sk",
    envvar="VIKINGDB_SK",
    required=True,
    help="VIKINGDB_SK",
)
@click.option(
    "--collection-name",
    envvar="COLLECTION_NAME",
    required=True,
    help="Collection name",
)
@click.option(
    "--index-name",
    envvar="INDEX_NAME",
    required=True,
    help="Index name",
)

def main(
    vikingdb_host: str, 
    vikingdb_region: str,
    vikingdb_ak: str,
    vikingdb_sk: str,
    collection_name: str,
    index_name: str,
):

    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = serve(
                vikingdb_host, 
                vikingdb_region, 
                vikingdb_ak, 
                vikingdb_sk,
                collection_name,
                index_name,
            )
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-server-vikingdb",
                    server_version="0.1.2",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())

