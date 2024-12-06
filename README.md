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

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-server-vikingdb": {
      "command": "uv",
      "args": [
        "--directory",
        "dir to mcp-server-vikingdb",
        "run",
        "mcp-server-vikingdb"
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
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-server-vikingdb": {
      "command": "uvx",
      "args": [
        "mcp-server-vikingdb"
      ]
    }
  }
  ```
</details>

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
npx @modelcontextprotocol/inspector uv --directory /Users/bytedance/Documents/workproject/mcp/mcp-server-vikingdb run mcp-server-vikingdb
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.