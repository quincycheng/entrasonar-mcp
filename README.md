# EntraSonar MCP

[![Python](https://img.shields.io/badge/Python->=3.10-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

A Model Context Protocol (MCP) server for intelligent Microsoft Entra ID and Azure infrastructure reconnaissance. Built with [FastMCP](https://github.com/jlopp/FastMCP), this server exposes powerful tools for domain intelligence, identity posture analysis, and M365 security insights.

## Overview

EntraSonar MCP leverages the [entrasonar.com](https://entrasonar.com/) platform to provide agents and applications with real-time access to:

- **Microsoft Entra ID reconnaissance** - Extract tenant identifiers, domain configurations, identity provider details, and cloud instance information
- **M365 security posture analysis** - Evaluate email security DNS records including SPF, DKIM, DMARC, MTA-STS, and BIMI configurations
- **Multi-cloud awareness** - Detect China cloud, Government cloud, and B2C tenant deployments

This server implements the MCP specification, allowing any MCP-compatible client to consume these tools for AI agents, automation workflows, and security assessments.

> [!NOTE]
> This is a reconnaissance and analysis tool. Use responsibly and ensure you have proper authorization before analyzing any domains or infrastructure.

## Features

- **Domain Intelligence** - Query comprehensive Microsoft Entra ID metadata including tenant IDs, domain types, federation configurations, and regional deployments
- **Email Security Assessment** - Analyze DNS security configurations for email delivery (MX, SPF, DKIM, DMARC)
- **Advanced DNS Hygiene** - Check for MTA-STS and BIMI adoption for enhanced email security
- **Identity Provider Detection** - Automatically identify and profile identity provider configurations
- **Multi-cloud Detection** - Determine cloud sovereignty and special deployments (Government, China, B2C)
- **Real-time Results** - Get fresh, up-to-date infrastructure analysis
- **Simple Tool Integration** - Use the `@mcp.tool()` decorator to extend functionality

## Prerequisites

- **Python 3.10+** - [Download Python](https://python.org/downloads)
- **uv** (optional but recommended) - Fast Python package installer. [Install uv](https://docs.astral.sh/uv/getting-started/)
- **Basic familiarity with MCP** - See [MCP documentation](https://modelcontextprotocol.io/introduction)

## Getting Started

### Quick Start with Local Environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd entrasonar-mcp
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the MCP server**
   ```bash
   uv run python main.py
   ```

   The server will start on **port 8000** using Streamable HTTP transport.

### Alternative: Install with pip

If you don't have `uv` installed:

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

> [!TIP]
> For development, consider using [uv](https://docs.astral.sh/uv/) as it's faster and handles dependencies more reliably than pip.

## Running the Server

### Development Mode

```bash
uv run python main.py
```

The MCP server exposes tools that can be called by any MCP-compatible client. The Streamable HTTP transport on port 8000 allows clients to connect and invoke tools.

### Docker Deployment

You can also run the server in a Docker container:

```bash
docker build -t entrasonar-mcp .
docker run -p 8000:8000 entrasonar-mcp
```

## Using the Tools

Once the MCP server is running, clients can invoke the available tools:

### Example: Query Domain Information

MCP clients can invoke the domain analysis tools to get:

```json
{
  "domain_info": {
    "tenantId": "12345678-1234-1234-1234-123456789012",
    "domain": "contoso.com",
    "domainType": "Managed",
    "displayName": "Contoso Corporation",
    "region": "US",
    "cloudInstanceName": "AzurePublic"
  },
  "m365_checks": {
    "emailSecurity": {
      "spf": { "configured": true, "record": "v=spf1 ..." },
      "dkim": { "configured": true },
      "dmarc": { "configured": true, "policy": "quarantine" }
    }
  }
}
```

## Adding Custom Tools

Extend the server with custom tools using the `@mcp.tool()` decorator:

```python
@mcp.tool(
    output_schema={
        "type": "object",
        "properties": {
            "result": {"type": "string", "description": "The result"}
        }
    }
)
def my_custom_tool(domain: str) -> dict:
    """Analyze a specific aspect of a domain."""
    # Your implementation here
    return {"result": "analysis data"}
```

Tools are automatically exposed to MCP clients once defined.

## Project Structure

```
entrasonar-mcp/
├── main.py              # MCP server implementation with tools
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
├── README.md            # This file
└── .gitignore          # Git ignore rules
```

## Deployment

### Deploy to AgentCore

```bash
agentcore deploy
```

Follow the prompts to configure your deployment. Your MCP server will be accessible to all AgentCore agents.

### Deploy to Azure

You can containerize and deploy this server to Azure Container Instances, Azure App Service, or Kubernetes:

```bash
# Build the Docker image
docker build -t entrasonar-mcp:latest .

# Tag for your registry
docker tag entrasonar-mcp:latest <your-registry>/entrasonar-mcp:latest

# Push to registry
docker push <your-registry>/entrasonar-mcp:latest

# Deploy using Azure CLI or your preferred method
az container create --resource-group <rg> \
  --name entrasonar-mcp \
  --image <your-registry>/entrasonar-mcp:latest \
  --ports 8000
```

## Configuration

The server can be configured through environment variables or direct modification of `main.py`:

- **Port** - Default is `8000`
- **User-Agent** - Customizable in the HEADERS dictionary
- **Tool Schemas** - Modify `output_schema` parameters in tool decorators

## Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlopp/FastMCP)
- [EntraSonar Platform](https://entrasonar.com/)
- [Python httpx Documentation](https://www.python-httpx.org/)

## Troubleshooting

### Server fails to start on port 8000

**Problem**: "Address already in use" error
- **Solution**: Change the port in `main.py` or kill the process using port 8000:
  ```bash
  lsof -ti:8000 | xargs kill -9
  ```

### MCP client can't connect

**Problem**: Connection refused when connecting to localhost:8000
- **Solution**: Ensure the server is running and accessible:
  ```bash
  curl http://localhost:8000/health  # If health endpoint exists
  ```

### Missing dependencies

**Problem**: `ModuleNotFoundError` when running `python main.py`
- **Solution**: Reinstall dependencies:
  ```bash
  uv sync --fresh
  # or
  pip install -r requirements.txt
  ```

## Getting Help

- **Issues & Bugs**: [Open an issue](https://github.com/your-repo/issues) on GitHub
- **MCP Questions**: Visit the [MCP Community](https://modelcontextprotocol.io/community)
- **EntraSonar Support**: Check [entrasonar.com](https://entrasonar.com/) documentation

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
