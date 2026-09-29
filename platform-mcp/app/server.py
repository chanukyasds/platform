from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from app.core.config import (
    MCP_PUBLIC_HOST,
    MCP_PUBLIC_ORIGIN,
)
from app.tools.argocd import register_argocd_tools
from app.tools.github import register_github_tools
from app.tools.kubernetes import register_kubernetes_tools
from app.tools.postgres import register_postgres_tools


mcp = MCPServer(
    "Platform MCP",
    description="MCP server for Platform and DBA operations",
    version="0.1.0",
)

register_postgres_tools(mcp)
register_kubernetes_tools(mcp)
register_argocd_tools(mcp)
register_github_tools(mcp)


if __name__ == "__main__":
    security = TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            MCP_PUBLIC_HOST,
            f"{MCP_PUBLIC_HOST}:*",
            "127.0.0.1:*",
            "localhost:*",
        ],
        allowed_origins=[
            MCP_PUBLIC_ORIGIN,
            "http://127.0.0.1:*",
            "http://localhost:*",
        ],
    )

    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=9000,
        transport_security=security,
    )