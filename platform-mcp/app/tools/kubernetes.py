from app.clients.platform_api import PlatformAPIClient


platform_api = PlatformAPIClient()


def register_kubernetes_tools(mcp):

    @mcp.tool()
    def kubernetes_get_nodes(
        cluster: str,
    ) -> dict:
        """
        Get Kubernetes nodes and their current status.

        Args:
            cluster: Kubernetes cluster name, for example k8s01.
        """
        return platform_api.kubernetes_get_nodes(cluster)

    @mcp.tool()
    def kubernetes_get_deployments(
        cluster: str,
    ) -> dict:
        """
        Get all deployments across namespaces in a Kubernetes cluster.

        Args:
            cluster: Kubernetes cluster name, for example k8s01.
        """
        return platform_api.kubernetes_get_deployments(cluster)

    @mcp.tool()
    def kubernetes_get_deployment(
        cluster: str,
        namespace: str,
        name: str,
    ) -> dict:
        """
        Get details of a specific Kubernetes deployment.

        Args:
            cluster: Kubernetes cluster name.
            namespace: Kubernetes namespace.
            name: Deployment name.
        """
        return platform_api.kubernetes_get_deployment(
            cluster,
            namespace,
            name,
        )

    @mcp.tool()
    def kubernetes_get_statefulsets(
        cluster: str,
    ) -> dict:
        """
        Get all StatefulSets in a Kubernetes cluster.

        Args:
            cluster: Kubernetes cluster name, for example k8s01.
        """
        return platform_api.kubernetes_get_statefulsets(cluster)

    @mcp.tool()
    def kubernetes_get_statefulset(
        cluster: str,
        namespace: str,
        name: str,
    ) -> dict:
        """
        Get details of a specific Kubernetes StatefulSet.

        Args:
            cluster: Kubernetes cluster name.
            namespace: Kubernetes namespace.
            name: StatefulSet name.
        """
        return platform_api.kubernetes_get_statefulset(
            cluster,
            namespace,
            name,
        )