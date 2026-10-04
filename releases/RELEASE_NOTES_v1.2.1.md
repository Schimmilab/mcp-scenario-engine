# Release Notes v1.2.1

**Distribution Release — prebuilt container image on GHCR** 📦

No code changes. From this release on, every version is published as a container image, so you can use the server without cloning the repo or setting up Python:

```bash
docker pull ghcr.io/schimmilab/mcp-scenario-engine:1.2.1
```

MCP client config:

```json
{
  "mcpServers": {
    "scenario-engine": {
      "command": "docker",
      "args": ["run", "-i", "--rm",
               "-v", "scenario-engine-data:/root/.mcp-scenario-engine",
               "ghcr.io/schimmilab/mcp-scenario-engine:1.2.1"]
    }
  }
}
```

Before the image is pushed, the release workflow starts it and performs a real MCP handshake (`initialize` + `tools/list`). An image that builds but doesn't answer is never published.
