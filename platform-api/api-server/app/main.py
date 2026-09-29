from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.postgres import router as postgres_router
from app.api.kubernetes import router as kubernetes_router
from app.api.argocd import router as argocd_router
from app.api.github import router as github_router


app = FastAPI(
    title="Platform API",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(postgres_router)
app.include_router(kubernetes_router)
app.include_router(argocd_router)
app.include_router(github_router)