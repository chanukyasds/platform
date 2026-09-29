import httpx

from fastapi import APIRouter, HTTPException

from app.services.github_service import GitHubService


router = APIRouter(
    prefix="/v1/github",
    tags=["GitHub"],
)

service = GitHubService()


@router.get("/repos/{repository_name}")
def get_repository(repository_name: str):

    try:
        repository = service.get_repository(
            repository_name
        )

        return {
            "repository": repository_name,
            "details": repository,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub API failed: {exc.response.text}",
        )


@router.get("/repos/{repository_name}/latest-commit")
def get_latest_commit(repository_name: str):

    try:
        commit = service.get_latest_commit(
            repository_name
        )

        return {
            "repository": repository_name,
            "commit": commit,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub API failed: {exc.response.text}",
        )


@router.get("/repos/{repository_name}/latest-release")
def get_latest_release(repository_name: str):

    try:
        release = service.get_latest_release(
            repository_name
        )

        return {
            "repository": repository_name,
            "release": release,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub API failed: {exc.response.text}",
        )


@router.get("/repos/{repository_name}/tree")
def get_tree(repository_name: str):

    try:
        tree = service.get_tree(repository_name)

        return {
            "repository": repository_name,
            "count": len(tree),
            "tree": tree,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub API failed: {exc.response.text}",
        )


@router.get("/repos/{repository_name}/files/{path:path}")
def get_file(
    repository_name: str,
    path: str,
):

    try:
        file = service.get_file(
            repository_name,
            path,
        )

        return {
            "repository": repository_name,
            "file": file,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub API failed: {exc.response.text}",
        )

@router.post(
    "/repos/{repository_name}/pull-requests/{pr_number}/merge"
)
def merge_pull_request(
    repository_name: str,
    pr_number: int,
):
    try:
        result = service.merge_pull_request(
            repository_name,
            pr_number,
        )

        return {
            "repository": repository_name,
            "pull_request": pr_number,
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
            detail=f"GitHub merge failed: {exc}",
        )