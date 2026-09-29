# Platform API

Backend control layer for platform and DBA operations.

`platform-api` exposes REST endpoints for PostgreSQL, Kubernetes, Argo CD, and GitHub integrations.

It is responsible for validation, credentials, backend communication, and operational policy.

## Architecture

```text
Client / MCP
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

The API follows a simple structure:

```text
Router
  ↓
Service
  ↓
Client
  ↓
Backend
```

## Structure

```text
platform-api/
├── .env.example
├── api-server/
│   ├── app/
│   │   ├── api/
│   │   ├── clients/
│   │   ├── config/
│   │   ├── core/
│   │   ├── models/
│   │   ├── security/
│   │   ├── services/
│   │   └── main.py
│   ├── config/
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
└── README.md
```

## Configuration

Create the environment file:

```bash
cp platform-api/.env.example platform-api/.env
```

Typical variables include:

```text
POSTGRES_USER
POSTGRES_PASSWORD
K8S_API_TOKEN
ARGOCD_API_TOKEN
GITHUB_API_TOKEN
```

Create local backend configuration from the examples:

```bash
cp platform-api/api-server/config/clusters.example.yaml \
   platform-api/api-server/config/clusters.yaml

cp platform-api/api-server/config/kubernetes.example.yaml \
   platform-api/api-server/config/kubernetes.yaml

cp platform-api/api-server/config/argocd.example.yaml \
   platform-api/api-server/config/argocd.yaml

cp platform-api/api-server/config/repositories.example.yaml \
   platform-api/api-server/config/repositories.yaml
```

Update these files for your environment.

Real `.env` and backend configuration files are excluded from Git.

## Run Locally

```bash
cd platform-api/api-server

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000
```

API documentation:

```text
http://localhost:8000/docs
```

## Install as a Service

From the repository root:

```bash
sudo python3 infra/scripts/install.py api
```

This installs the Python environment and configures:

```text
platform-api.service
```

## Current Integrations

- PostgreSQL
- Kubernetes
- Argo CD
- GitHub

## Security

`platform-api` is the trusted backend layer.

Infrastructure credentials stay here and are not exposed to MCP clients.

Write operations should use:

- explicit validation
- allowlists where appropriate
- existing backend RBAC
- existing approval and change-control mechanisms

Sensitive values should never be committed to the repository.