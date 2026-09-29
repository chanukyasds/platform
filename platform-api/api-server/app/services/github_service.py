from app.clients.github_client import GitHubClient
from app.core.config import load_repositories


class GitHubService:

    def __init__(self):
        self.repositories = load_repositories()

    def _get_client(
        self,
        repository_name: str,
    ) -> GitHubClient:

        repository = self.repositories.get(
            repository_name
        )

        if repository is None:
            raise ValueError(
                f"Unknown repository: {repository_name}"
            )

        return GitHubClient(
            owner=repository["owner"],
            repo=repository["repo"],
            branch=repository.get(
                "branch",
                "main",
            ),
        )

    def get_repository(
        self,
        repository_name: str,
    ):
        client = self._get_client(repository_name)

        return client.get_repository()

    def get_latest_commit(
        self,
        repository_name: str,
    ):
        client = self._get_client(repository_name)

        return client.get_latest_commit()

    def get_latest_release(
        self,
        repository_name: str,
    ):
        client = self._get_client(repository_name)

        return client.get_latest_release()

    def get_tree(
        self,
        repository_name: str,
    ):
        client = self._get_client(repository_name)

        return client.get_tree()

    def get_file(
        self,
        repository_name: str,
        path: str,
    ):
        client = self._get_client(repository_name)

        return client.get_file(path)

    def merge_pull_request(
        self,
        repository_name: str,
        pr_number: int,
    ):
        client = self._get_client(repository_name)

        return client.merge_pull_request_if_ready(
            pr_number
        )