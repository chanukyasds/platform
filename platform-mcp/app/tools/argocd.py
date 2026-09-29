from app.clients.platform_api import PlatformAPIClient


platform_api = PlatformAPIClient()


def register_argocd_tools(mcp):

    @mcp.tool()
    def argocd_get_applications(
        cluster: str,
    ) -> dict:
        """
        Get all Argo CD applications and their sync and health status.

        Args:
            cluster: Argo CD cluster name, for example argocd01.
        """
        return platform_api.argocd_get_applications(cluster)

    @mcp.tool()
    def argocd_get_application(
        cluster: str,
        application: str,
    ) -> dict:
        """
        Get detailed status for a specific Argo CD application.

        Args:
            cluster: Argo CD cluster name.
            application: Argo CD application name.
        """
        return platform_api.argocd_get_application(
            cluster,
            application,
        )
    
    @mcp.tool(name="argocd_sync_application")
    def sync_application(
        cluster: str,
        application_name: str,
    ) -> dict:
        """
        Sync an Argo CD application to its desired Git state.
        """
        return platform_api.argocd_sync_application(
            cluster,
            application_name,
        )