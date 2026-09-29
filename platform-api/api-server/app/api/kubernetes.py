from fastapi import APIRouter, HTTPException

from app.services.kubernetes_service import KubernetesService


router = APIRouter(
    prefix="/v1/kubernetes",
    tags=["Kubernetes"],
)

service = KubernetesService()


@router.get("/clusters/{cluster_name}/nodes")
def get_nodes(cluster_name: str):

    try:
        nodes = service.get_nodes(cluster_name)

        return {
            "cluster": cluster_name,
            "count": len(nodes),
            "nodes": nodes,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes API failed: {exc}",
        )

@router.get("/clusters/{cluster_name}/namespaces")
def get_namespaces(cluster_name: str):

    try:
        namespaces = service.get_namespaces(cluster_name)

        return {
            "cluster": cluster_name,
            "count": len(namespaces),
            "namespaces": namespaces,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes API failed: {exc}",
        )


@router.get("/clusters/{cluster_name}/deployments")
def get_deployments(cluster_name: str):

    try:
        deployments = service.get_deployments(cluster_name)

        return {
            "cluster": cluster_name,
            "count": len(deployments),
            "deployments": deployments,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes API failed: {exc}",
        )


@router.get(
    "/clusters/{cluster_name}/deployments/{namespace}/{name}"
)
def get_deployment(cluster_name: str,namespace: str,name: str,):

    try:
        deployment = service.get_deployment(
            cluster_name=cluster_name,
            namespace=namespace,
            name=name,
        )

        return {
            "cluster": cluster_name,
            "deployment": deployment,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes API failed: {exc}",
        )

@router.get("/clusters/{cluster_name}/statefulsets")
def get_statefulsets(cluster_name: str):

    try:
        statefulsets = service.get_statefulsets(cluster_name)

        return {
            "cluster": cluster_name,
            "count": len(statefulsets),
            "statefulsets": statefulsets,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes API failed: {exc}",
        )


@router.get(
    "/clusters/{cluster_name}/statefulsets/{namespace}/{name}"
)
def get_statefulset(
    cluster_name: str,
    namespace: str,
    name: str,
):

    try:
        statefulset = service.get_statefulset(
            cluster_name=cluster_name,
            namespace=namespace,
            name=name,
        )

        return {
            "cluster": cluster_name,
            "statefulset": statefulset,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Kubernetes API failed: {exc}",
        )