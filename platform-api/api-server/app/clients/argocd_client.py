import os

import httpx


class ArgoCDClient:

    def __init__(
        self,
        server: str,
        verify_ssl: bool = True,
    ):
        token = os.environ["ARGOCD_API_TOKEN"]

        self.server = server.rstrip("/")

        self.client = httpx.Client(
            base_url=self.server,
            verify=verify_ssl,
            timeout=10.0,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

    def get_applications(self) -> list[dict]:

        response = self.client.get(
            "/api/v1/applications"
        )

        response.raise_for_status()

        data = response.json()

        applications = []

        for app in data.get("items", []):

            metadata = app.get("metadata", {})
            spec = app.get("spec", {})
            status = app.get("status", {})

            applications.append(
                {
                    "name": metadata.get("name"),
                    "namespace": metadata.get("namespace"),
                    "project": spec.get("project"),
                    "health": status.get(
                        "health", {}
                    ).get("status"),
                    "sync_status": status.get(
                        "sync", {}
                    ).get("status"),
                    "revision": status.get(
                        "sync", {}
                    ).get("revision"),
                }
            )

        return applications

    def get_application(
        self,
        application_name: str,
    ) -> dict:

        response = self.client.get(
            f"/api/v1/applications/{application_name}"
        )

        response.raise_for_status()

        app = response.json()

        metadata = app.get("metadata", {})
        spec = app.get("spec", {})
        status = app.get("status", {})

        source = spec.get("source", {})
        destination = spec.get("destination", {})
        health = status.get("health", {})
        sync = status.get("sync", {})

        operation_state = status.get(
            "operationState", {}
        )

        return {
            "name": metadata.get("name"),
            "namespace": metadata.get("namespace"),
            "project": spec.get("project"),

            "health": health.get("status"),

            "sync_status": sync.get("status"),
            "revision": sync.get("revision"),

            "repository": source.get("repoURL"),
            "path": source.get("path"),
            "target_revision":
                source.get("targetRevision"),

            "destination": {
                "server": destination.get("server"),
                "namespace":
                    destination.get("namespace"),
            },

            "last_operation": {
                "phase":
                    operation_state.get("phase"),
                "message":
                    operation_state.get("message"),
                "started_at":
                    operation_state.get("startedAt"),
                "finished_at":
                    operation_state.get("finishedAt"),
            },
        }
    
    def sync_application(
        self,
        application_name: str,
    ) -> dict:

        response = self.client.post(
            f"/api/v1/applications/{application_name}/sync",
            json={},
        )

        if response.status_code == 404:
            raise ValueError(
                f"Argo CD application '{application_name}' does not exist"
            )

        if not response.is_success:
            raise ValueError(
                f"Argo CD sync failed "
                f"({response.status_code}): "
                f"{response.text}"
            )

        return response.json()