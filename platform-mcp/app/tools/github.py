from app.clients.platform_api import PlatformAPIClient


platform_api = PlatformAPIClient()


def register_github_tools(mcp):

    @mcp.tool()
    def github_get_latest_commit(
        repository: str,
    ) -> dict:
        """
        Get the latest commit from a configured GitHub repository.

        Args:
            repository: Repository alias, for example kubernetes.
        """
        return platform_api.github_get_latest_commit(
            repository
        )

    @mcp.tool()
    def github_get_file(
        repository: str,
        path: str,
    ) -> dict:
        """
        Read a file from a configured GitHub repository.

        Useful for reading Kubernetes manifests and configuration files.

        Args:
            repository: Repository alias, for example kubernetes.
            path: Path to the file inside the repository.
        """
        return platform_api.github_get_file(
            repository,
            path,
        )
    @mcp.tool()
    def merge_pull_request(
        repository_name: str,
        pr_number: int,
    ) -> dict:
        """
        Merge a pull request only if the Platform API confirms
        that it is approved, CI checks have passed, and the PR
        is mergeable.
        """
        return platform_api.merge_pull_request(
            repository_name,
            pr_number,
        )