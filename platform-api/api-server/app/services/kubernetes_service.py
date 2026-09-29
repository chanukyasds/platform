from app.clients.kubernetes_client import KubernetesClient
from app.core.config import load_kubernetes_clusters


class KubernetesService:

    def __init__(self):
        self.clusters = load_kubernetes_clusters()

    def _get_client(
        self,
        cluster_name: str,
    ) -> KubernetesClient:

        cluster = self.clusters.get(cluster_name)

        if cluster is None:
            raise ValueError(
                f"Unknown Kubernetes cluster: {cluster_name}"
            )

        return KubernetesClient(
            api_server=cluster["api_server"],
            ca_cert=cluster["ca_cert"],
        )

    def get_nodes(self, cluster_name: str):

        client = self._get_client(cluster_name)

        return client.get_nodes()

    def get_namespaces(self,cluster_name: str,):
        client = self._get_client(cluster_name)

        return client.get_namespaces()


    def get_deployments(self,cluster_name: str,):
        client = self._get_client(cluster_name)

        return client.get_deployments()


    def get_deployment(self,cluster_name: str,namespace: str,name: str,):
        client = self._get_client(cluster_name)

        return client.get_deployment(
            namespace=namespace,
            name=name,
        )

    def get_statefulsets(
        self,
        cluster_name: str,
    ):
        client = self._get_client(cluster_name)
        return client.get_statefulsets()


    def get_statefulset(
        self,
        cluster_name: str,
        namespace: str,
        name: str,
    ):
        client = self._get_client(cluster_name)

        return client.get_statefulset(
            namespace=namespace,
            name=name,
        )