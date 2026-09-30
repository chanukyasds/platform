
# Platform - AI Assisted Infrastructure and DBA Operations

A modular platform automation project that exposes infrastructure and DBA operations through a controlled REST API and MCP interface.

## Architecture

```
AI Clients
(Gemini, Claude, MCP-compatible clients)
                │
                ▼
        ┌─────────────────┐
        │  platform-mcp   │
        │ AI-facing tools │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  platform-api   │
        │ Policy, auth,   │
        │ validation      │
        └────────┬────────┘
                 │
      ┌──────────┼──────────┬──────────┐
      ▼          ▼          ▼          ▼
 PostgreSQL   Kubernetes   Argo CD    GitHub
```


`platform-mcp` does not connect directly to infrastructure.

All backend access, credentials, validation, and operational controls are handled by `platform-api`.

## Available MCP Actions

### PostgreSQL

- Get settings
- Get single setting
- Reload configuration
- Set allowlisted parameter
- List databases
- Analyze table
- Vacuum table
- Check PostgreSQL SQL files
- Trigger checkpoint
- Get uptime
- Get active replication slots

### Kubernetes

- Get nodes
- Get deployments
- Get deployment
- Get StatefulSets
- Get StatefulSet

### Argo CD

- Get applications
- Get application
- Sync application

### GitHub

- Get file
- Get latest commit
- Merge pull request

> Actions are exposed through `platform-mcp` and delegated to `platform-api` for validation and backend execution.


## Repository

```
platform/
├── platform-api/
├── platform-mcp/
├── skills/
├── infra/
├── docs/
└── README.md
```

## Configuration

Environment-specific configuration and secrets are excluded from Git.

Create local files from the provided examples.

### Platform API

```bash
cp platform-api/.env.example platform-api/.env

cp platform-api/api-server/config/clusters.example.yaml \
   platform-api/api-server/config/clusters.yaml

cp platform-api/api-server/config/kubernetes.example.yaml \
   platform-api/api-server/config/kubernetes.yaml

cp platform-api/api-server/config/argocd.example.yaml \
   platform-api/api-server/config/argocd.yaml

cp platform-api/api-server/config/repositories.example.yaml \
   platform-api/api-server/config/repositories.yaml
```

### Platform MCP

```bash
cp platform-mcp/.env.example platform-mcp/.env
```

## Installation

Install Platform API:

```bash
sudo python3 infra/scripts/install.py api
```

Install Platform MCP:

```bash
sudo python3 infra/scripts/install.py mcp
```

## Security Model

```text
AI Client(LLM)
     │
     ▼
    MCP
     │
     ▼
Platform API
     │
     ▼
Infrastructure
```

Infrastructure credentials remain in `platform-api`.

Write operations should use explicit validation, allowlists, backend RBAC, and existing infrastructure controls.

## Status

Current integrations include:

- PostgreSQL
- Kubernetes
- Argo CD
- GitHub

The project is under active development.