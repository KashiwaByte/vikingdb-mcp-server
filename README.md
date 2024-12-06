# VikingDB MCP server

a mcp server for vikingdb store and search

## Components



### Tools

The server implements one tool:
- vikingdb-upsert-information: upsert information to vikingdb for later use

- vikingdb-search-information: Searches for information in the VikingDB
  
  
## Configuration

[TODO: Add configuration details specific to your implementation]

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Development/Unpublished Servers Configuration
```
{
  "mcpServers": {
    "mcp-server-vikingdb": {
      "command": "uv",
      "args": [
        "--directory",
        "dir to mcp-server-vikingdb",
        "run",
        "mcp-server-vikingdb",
        "--vikingdb-host", 
        "your host",
        "--vikingdb-region", 
        "your region",
        "--vikingdb-ak", 
        "your access key",
        "--vikingdb-sk", 
        "your secret key",
        "--collection-name",
        "your collection name",
        "--index-name",
        "your index name"
      ]
    }
  }
}

  ```

Published Servers Configuration
  ```
{
    "mcpServers": {
      "mcp-server-vikingdb": {
        "command": "uvx",
        "args": [
          "mcp-server-vikingdb"
      ]
     }
    }
  } 
  ```


## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory dir_to_mcp_server_vikingdb run mcp-server-vikingdb --vikingdb-host your_host --vikingdb-region your_region --vikingdb-ak your_access_key --vikingdb-sk your_secret_key --collection-name your_collection_name --index-name your_index_name
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.