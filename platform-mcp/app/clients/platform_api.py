import httpx

from app.core.config import PLATFORM_API_URL


class PlatformAPIClient:

    def __init__(self):
        self.client = httpx.Client(
            base_url=PLATFORM_API_URL,
            timeout=15.0,
        )

    def _get(self, path: str) -> dict:
        response = self.client.get(path)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str) -> dict:
        response = self.client.post(path)
        response.raise_for_status()
        return response.json()

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    def health(self) -> dict:
        return self._get("/health")

    # ---------------------------------------------------------
    # PostgreSQL
    # ---------------------------------------------------------

    def postgres_get_setting(
        self,
        cluster: str,
        parameter: str,
    ) -> dict:
        return self._get(
            f"/v1/postgres/clusters/{cluster}/settings/{parameter}"
        )

    def postgres_get_settings(
        self,
        cluster: str,
    ) -> dict:
        return self._get(
            f"/v1/postgres/clusters/{cluster}/settings"
        )

    def postgres_reload(self, cluster: str) -> dict:
        return self._post(
            f"/v1/postgres/clusters/{cluster}/reload"
        )

    def postgres_uptime(self, cluster: str) -> dict:
        return self._post(
            f"/v1/postgres/clusters/{cluster}/uptime"
        )

    def postgres_get_databases(self, cluster: str) -> dict:
        return self._get(
            f"/v1/postgres/clusters/{cluster}/databases"
        )

    def postgres_checkpoint(
        self,
        cluster: str,
    ) -> dict:
        return self._post(
            f"/v1/postgres/clusters/{cluster}/checkpoint"
        )
    
    def postgres_get_active_replication_slots(self, cluster: str) -> dict:
        return self._get(
            f"/v1/postgres/clusters/{cluster}/get_active_replication_slots"
        )

    def postgres_analyze_table(
        self,
        cluster: str,
        table_name: str,
    ) -> dict:
        return self._post(
            f"/v1/postgres/clusters/{cluster}/analyze/{table_name}"
        )

    def postgres_vacuum_table(
        self,
        cluster: str,
        table_name: str,
    ) -> dict:
        return self._post(
            f"/v1/postgres/clusters/{cluster}/vacuum/{table_name}"
        )

    def _post(
        self,
        path: str,
        params: dict | None = None,
    ) -> dict:
        response = self.client.post(
            path,
            params=params,
        )
        response.raise_for_status()
        return response.json()

    def postgres_set_parameter(
        self,
        cluster: str,
        parameter: str,
        value: str,
    ) -> dict:

        try:
            return self._post(
                f"/v1/postgres/clusters/{cluster}/postgres_set_parameter",
                params={
                    "parameter": parameter,
                    "value": value,
                },
            )

        except httpx.HTTPStatusError as exc:
            response = exc.response

            try:
                detail = response.json().get(
                    "detail",
                    response.text,
                )
            except Exception:
                detail = response.text

            return detail

    def check_postgres(
        self,
        cluster: str,
        mode: str,
    ) -> dict:
        return self._post(
            f"/v1/postgres/clusters/{cluster}/check_postgres",
            params={
                "mode": mode,
            },
        )

    # ---------------------------------------------------------
    # Kubernetes
    # ---------------------------------------------------------

    def kubernetes_get_nodes(
        self,
        cluster: str,
    ) -> dict:
        return self._get(
            f"/v1/kubernetes/clusters/{cluster}/nodes"
        )

    def kubernetes_get_deployments(
        self,
        cluster: str,
    ) -> dict:
        return self._get(
            f"/v1/kubernetes/clusters/{cluster}/deployments"
        )

    def kubernetes_get_deployment(
        self,
        cluster: str,
        namespace: str,
        name: str,
    ) -> dict:
        return self._get(
            f"/v1/kubernetes/clusters/{cluster}"
            f"/deployments/{namespace}/{name}"
        )

    def kubernetes_get_statefulsets(
        self,
        cluster: str,
    ) -> dict:
        return self._get(
            f"/v1/kubernetes/clusters/{cluster}/statefulsets"
        )

    def kubernetes_get_statefulset(
        self,
        cluster: str,
        namespace: str,
        name: str,
    ) -> dict:
        return self._get(
            f"/v1/kubernetes/clusters/{cluster}"
            f"/statefulsets/{namespace}/{name}"
        )

    # ---------------------------------------------------------
    # Argo CD
    # ---------------------------------------------------------

    def argocd_get_applications(
        self,
        cluster: str,
    ) -> dict:
        return self._get(
            f"/v1/argocd/clusters/{cluster}/applications"
        )

    def argocd_get_application(
        self,
        cluster: str,
        application: str,
    ) -> dict:
        return self._get(
            f"/v1/argocd/clusters/{cluster}"
            f"/applications/{application}"
        )

    def argocd_sync_application(
        self,
        cluster: str,
        application_name: str,
    ) -> dict:
        return self._post(
            f"/v1/argocd/clusters/{cluster}/applications/{application_name}/sync"
        )

    # ---------------------------------------------------------
    # GitHub
    # ---------------------------------------------------------

    def github_get_latest_commit(
        self,
        repository: str,
    ) -> dict:
        return self._get(
            f"/v1/github/repos/{repository}/latest-commit"
        )

    def github_get_file(
        self,
        repository: str,
        path: str,
    ) -> dict:
        return self._get(
            f"/v1/github/repos/{repository}/files/{path}"
        )

    def merge_pull_request(
        self,
        repository_name: str,
        pr_number: int,
    ) -> dict:
        return self._post(
            f"/v1/github/repos/{repository_name}/pull-requests/{pr_number}/merge"
        )