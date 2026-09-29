# Platform MCP

AI-facing MCP server for platform and DBA operations.

`platform-mcp` exposes selected operational capabilities as MCP tools and forwards requests to `platform-api`.

It does not connect directly to PostgreSQL, Kubernetes, Argo CD, or GitHub.

## Architecture

```text
AI Clients
    │
    ▼
┌──────────────────────────┐
│      platform-mcp        │
│   MCP tools / gateway    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      platform-api        │
│ Validation • Policy      │
│ Credentials • Backends   │
└────────────┬─────────────┘
             │
   ┌─────────┼─────────┬─────────┐
   ▼         ▼         ▼         ▼
PostgreSQL Kubernetes Argo CD  GitHub
```

## Structure

```text
platform-mcp/
├── .env.example
├── app/
│   ├── tools/
│   │   ├── postgres.py
│   │   ├── kubernetes.py
│   │   ├── argocd.py
│   │   └── github.py
│   ├── core/
│   ├── platform_api.py
│   └── server.py
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Configuration

Create the local environment file:

```bash
cp platform-mcp/.env.example platform-mcp/.env
```

Typical variables include:

```text
PLATFORM_API_URL
MCP_PUBLIC_HOST
MCP_PUBLIC_ORIGIN
```

Example local setup:

```text
PLATFORM_API_URL=http://localhost:8000
MCP_PUBLIC_HOST=localhost
MCP_PUBLIC_ORIGIN=http://localhost
```

The real `.env` file is excluded from Git.

## Run Locally

```bash
cd platform-mcp

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python -m app.server
```

Default MCP port:

```text
9000
```

Transport:

```text
Streamable HTTP
```

## Install as a Service

From the repository root:

```bash
sudo python3 infra/scripts/install.py mcp
```

This installs the Python environment and configures:

```text
platform-mcp.service
```

## Current Tool Domains

- PostgreSQL
- Kubernetes
- Argo CD
- GitHub

MCP tools should remain thin and delegate backend logic to `platform-api`.

## Security

`platform-mcp` should not contain infrastructure credentials.

The intended trust boundary is:

```text
AI Client
    │
    ▼
Platform MCP
    │
    ▼
Platform API
    │
    ▼
Infrastructure
```

Authentication should be added before exposing MCP to production environments.

Sensitive values should never be committed to the repository.