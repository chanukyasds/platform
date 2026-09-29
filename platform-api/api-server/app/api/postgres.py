from fastapi import APIRouter, HTTPException

from app.services.postgres_service import PostgresService


router = APIRouter(
    prefix="/v1/postgres",
    tags=["PostgreSQL"],
)

service = PostgresService()


@router.get("/clusters/{cluster_name}/settings")
def get_postgres_settings(cluster_name: str):

    try:
        settings = service.get_settings(cluster_name)

        return {
            "cluster": cluster_name,
            "count": len(settings),
            "settings": settings,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL connection failed: {exc}",
        )

@router.get("/clusters/{cluster_name}/settings/{parameter}")
def get_postgres_setting(
    cluster_name: str,
    parameter: str,
):

    try:
        setting = service.get_setting(
            cluster_name,
            parameter,
        )

        return {
            "cluster": cluster_name,
            "setting": setting,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL connection failed: {exc}",
        )


@router.post("/clusters/{cluster_name}/reload")
def reload_postgres_config(cluster_name: str):

    try:
        reloaded = service.reload_config(cluster_name)

        return {
            "cluster": cluster_name,
            "operation": "reload_config",
            "success": reloaded,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL reload failed: {exc}",
        )

@router.post("/clusters/{cluster_name}/uptime")
def uptime(cluster_name: str):

    try:
        uptime = service.uptime(cluster_name)

        return {
            "cluster": cluster_name,
            "success": uptime,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Fetching uptime failed: {exc}",
        )

@router.get("/clusters/{cluster_name}/databases")
def get_postgres_databases(cluster_name: str):
    try:
        databases = service.get_databases(cluster_name)

        return {
            "cluster": cluster_name,
            "databases": databases,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL database listing failed: {exc}",
        )

@router.post("/clusters/{cluster_name}/checkpoint")
def checkpoint_postgres(
    cluster_name: str,
):
    try:
        result = service.checkpoint(
            cluster_name
        )

        return {
            "cluster": cluster_name,
            "operation": "checkpoint",
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL checkpoint failed: {exc}",
        )

@router.get("/clusters/{cluster_name}/get_active_replication_slots")
def get_active_replication_slots(cluster_name: str):
    try:
        get_active_replication_slots = service.get_active_replication_slots(cluster_name)

        return {
            "cluster": cluster_name,
            "replication_slots": get_active_replication_slots,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL Fetching Active Replication Slots failed: {exc}",
        )

@router.post("/clusters/{cluster_name}/analyze/{table_name}")
def analyze_table(
    cluster_name: str,
    table_name: str,
):
    try:
        analyze = service.analyze_table(
            cluster_name,
            table_name,
        )

        return {
            "cluster": cluster_name,
            "analyze": analyze,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL analyze failed: {exc}",
        )

@router.post("/clusters/{cluster_name}/vacuum/{table_name}")
def vacuum_table(
    cluster_name: str,
    table_name: str,
):
    try:
        vacuum = service.vacuum_table(
            cluster_name,
            table_name,
        )

        return {
            "cluster": cluster_name,
            "vacuum": vacuum,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PostgreSQL vacuum failed: {exc}",
        )

@router.post(
    "/clusters/{cluster_name}/postgres_set_parameter"
)
def postgres_set_parameter(
    cluster_name: str,
    parameter: str,
    value: str,
):
    try:
        result = service.postgres_set_parameter(
            cluster_name,
            parameter,
            value,
        )

        return {
            "cluster": cluster_name,
            "parameter": parameter,
            "value": value,
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
            detail=f"PostgreSQL parameter update failed: {exc}",
        )

@router.post("/clusters/{cluster_name}/check_postgres")
def check_postgres(
    cluster_name: str,
    mode: str,
):
    try:
        result = service.check_postgres(
            cluster_name,
            mode,
        )

        return {
            "cluster": cluster_name,
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
            detail=f"PostgreSQL check failed: {exc}",
        )