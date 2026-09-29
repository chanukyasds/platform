from fastapi import APIRouter, HTTPException
import httpx

from app.services.argocd_service import ArgoCDService


router = APIRouter(
    prefix="/v1/argocd",
    tags=["Argo CD"],
)

service = ArgoCDService()


@router.get("/clusters/{cluster_name}/applications")
def get_applications(cluster_name: str):

    try:
        applications = service.get_applications(
            cluster_name
        )

        return {
            "cluster": cluster_name,
            "count": len(applications),
            "applications": applications,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Argo CD API failed: {exc.response.text}",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Argo CD API failed: {exc}",
        )


@router.get(
    "/clusters/{cluster_name}/applications/{application_name}"
)
def get_application(
    cluster_name: str,
    application_name: str,
):

    try:
        application = service.get_application(
            cluster_name,
            application_name,
        )

        return {
            "cluster": cluster_name,
            "application": application,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Argo CD API failed: {exc.response.text}",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Argo CD API failed: {exc}",
        )

@router.post(
    "/clusters/{cluster_name}/applications/{application_name}/sync"
)
def sync_application(
    cluster_name: str,
    application_name: str,
):
    try:
        result = service.sync_application(
            cluster_name,
            application_name,
        )

        return {
            "cluster": cluster_name,
            "application": application_name,
            "operation": "sync",
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Argo CD sync failed: {exc}",
        )