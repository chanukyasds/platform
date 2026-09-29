from app.clients.argocd_client import ArgoCDClient
from app.core.config import load_argocd_clusters


class ArgoCDService:

    def __init__(self):
        self.clusters = load_argocd_clusters()

    def _get_client(
        self,
        cluster_name: str,
    ) -> ArgoCDClient:

        cluster = self.clusters.get(cluster_name)

        if cluster is None:
            raise ValueError(
                f"Unknown Argo CD cluster: {cluster_name}"
            )

        return ArgoCDClient(
            server=cluster["server"],
            verify_ssl=cluster.get(
                "verify_ssl",
                True,
            ),
        )

    def get_applications(
        self,
        cluster_name: str,
    ):
        client = self._get_client(cluster_name)

        return client.get_applications()

    def get_application(
        self,
        cluster_name: str,
        application_name: str,
    ):
        client = self._get_client(cluster_name)

        return client.get_application(
            application_name
        )

    def sync_application(
        self,
        cluster_name: str,
        application: str,
    ):
        client = self._get_client(cluster_name)

        return client.sync_application(
            application
        )