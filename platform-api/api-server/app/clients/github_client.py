import base64
import os

import httpx


class GitHubClient:

    def __init__(
        self,
        owner: str,
        repo: str,
        branch: str = "main",
    ):
        self.owner = owner
        self.repo = repo
        self.branch = branch

        token = os.getenv("GITHUB_API_TOKEN")

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.Client(
            base_url="https://api.github.com",
            headers=headers,
            timeout=10.0,
        )

    def get_repository(self) -> dict:

        response = self.client.get(
            f"/repos/{self.owner}/{self.repo}"
        )

        response.raise_for_status()

        repo = response.json()

        return {
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "private": repo.get("private"),
            "default_branch": repo.get("default_branch"),
            "updated_at": repo.get("updated_at"),
        }

    def get_latest_commit(self) -> dict:

        response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/commits/{self.branch}"
        )

        response.raise_for_status()

        commit = response.json()

        commit_data = commit.get("commit", {})
        author = commit_data.get("author", {})

        return {
            "sha": commit.get("sha"),
            "short_sha": (
                commit.get("sha", "")[:7]
            ),
            "message": commit_data.get("message"),
            "author": author.get("name"),
            "date": author.get("date"),
            "url": commit.get("html_url"),
        }

    def get_latest_release(self) -> dict:

        response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/releases/latest"
        )

        response.raise_for_status()

        release = response.json()

        return {
            "name": release.get("name"),
            "tag": release.get("tag_name"),
            "published_at": release.get("published_at"),
            "prerelease": release.get("prerelease"),
            "draft": release.get("draft"),
            "url": release.get("html_url"),
        }

    def get_tree(self) -> list[dict]:

        response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/git/trees/{self.branch}",
            params={
                "recursive": "1",
            },
        )

        response.raise_for_status()

        data = response.json()

        files = []

        for item in data.get("tree", []):
            files.append(
                {
                    "path": item.get("path"),
                    "type": item.get("type"),
                    "sha": item.get("sha"),
                    "size": item.get("size"),
                }
            )

        return files

    def get_file(
        self,
        path: str,
    ) -> dict:

        response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/contents/{path}",
            params={
                "ref": self.branch,
            },
        )

        response.raise_for_status()

        file = response.json()

        content = file.get("content")

        decoded_content = None

        if content and file.get("encoding") == "base64":
            decoded_content = base64.b64decode(
                content
            ).decode("utf-8")

        return {
            "name": file.get("name"),
            "path": file.get("path"),
            "sha": file.get("sha"),
            "size": file.get("size"),
            "content": decoded_content,
        }

    def merge_pull_request_if_ready(
        self,
        pr_number: int,
    ) -> dict:

        # 1. Get pull request
        pr_response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/pulls/{pr_number}"
        )

        if pr_response.status_code == 404:
            raise ValueError(
                f"Pull request #{pr_number} does not exist"
            )

        pr_response.raise_for_status()
        pr = pr_response.json()

        if pr["state"] != "open":
            raise ValueError(
                f"Pull request #{pr_number} is not open"
            )

        # 2. Check approvals
        reviews_response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/pulls/{pr_number}/reviews"
        )

        reviews_response.raise_for_status()
        reviews = reviews_response.json()

        approved = any(
            review["state"] == "APPROVED"
            for review in reviews
        )

        if not approved:
            raise ValueError(
                f"Pull request #{pr_number} is not approved"
            )

        # 3. Get PR head commit SHA
        head_sha = pr["head"]["sha"]

        # 4. Check GitHub check runs / CI
        checks_response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/commits/{head_sha}/check-runs"
        )

        checks_response.raise_for_status()
        checks = checks_response.json()

        check_runs = checks.get("check_runs", [])

        failed_checks = [
            check["name"]
            for check in check_runs
            if check.get("status") == "completed"
            and check.get("conclusion") not in (
                "success",
                "neutral",
                "skipped",
            )
        ]

        pending_checks = [
            check["name"]
            for check in check_runs
            if check.get("status") != "completed"
        ]

        if failed_checks:
            raise ValueError(
                "CI checks failed: "
                + ", ".join(failed_checks)
            )

        if pending_checks:
            raise ValueError(
                "CI checks still running: "
                + ", ".join(pending_checks)
            )

        # 5. Check classic commit status too
        status_response = self.client.get(
            f"/repos/{self.owner}/{self.repo}/commits/{head_sha}/status"
        )

        status_response.raise_for_status()
        status = status_response.json()

        statuses = status.get("statuses", [])

        if statuses:
            if status.get("state") == "failure":
                raise ValueError(
                    f"Commit status failed for pull request #{pr_number}"
                )

            if status.get("state") == "pending":
                raise ValueError(
                    f"Commit status is still pending for pull request #{pr_number}"
                )

        # 6. Mergeability
        if pr.get("mergeable") is False:
            raise ValueError(
                f"Pull request #{pr_number} is not mergeable"
            )

        # 7. Merge
        merge_response = self.client.put(
            f"/repos/{self.owner}/{self.repo}/pulls/{pr_number}/merge",
            json={
                "merge_method": "merge",
                "sha": head_sha,
            },
        )

        if not merge_response.is_success:
            raise ValueError(
                f"GitHub merge rejected "
                f"({merge_response.status_code}): "
                f"{merge_response.text}"
            )

        result = merge_response.json()

        return {
            "pull_request": pr_number,
            "approved": True,
            "ci_passed": True,
            "merged": result.get("merged", False),
            "message": result.get("message"),
            "sha": result.get("sha"),
        }