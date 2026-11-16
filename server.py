# INF601 - Advanced Programming in Python
# Khaleed Hossain
# Mini Project 7

"""MCP server that wraps the Practice Hub REST API.

Runs over stdio, so nothing may be printed to stdout (it carries the MCP
protocol). Any logging goes to stderr.
"""

import os
import sys

import httpx
from mcp.server.fastmcp import FastMCP

# --- Configuration (from environment, never hard-coded) -------------------
BASE = os.environ.get("PRACTICE_API_URL", "").rstrip("/")
TOKEN = os.environ.get("PRACTICE_API_TOKEN", "")

if not BASE or not TOKEN:
    print(
        "WARNING: PRACTICE_API_URL and PRACTICE_API_TOKEN must be set.",
        file=sys.stderr,
    )

mcp = FastMCP("practice-hub")


def _request(method: str, path: str, **kwargs):
    """Call the Practice Hub API; return parsed JSON or a readable error dict."""
    if not BASE or not TOKEN:
        return {"error": "Server is not configured: set PRACTICE_API_URL and "
                         "PRACTICE_API_TOKEN environment variables."}
    try:
        r = httpx.request(
            method,
            f"{BASE}{path}",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=15.0,
            **kwargs,
        )
    except httpx.HTTPError as exc:
        return {"error": f"Could not reach the Practice Hub API: {exc}"}

    if r.status_code >= 400:
        messages = {
            401: "Unauthorized: missing or invalid token. Check PRACTICE_API_TOKEN.",
            403: "Forbidden: you can only modify or delete your own posts.",
            404: "Not found: no post exists with that id.",
            422: "Invalid input: the API rejected the submitted data.",
        }
        detail = r.text[:300]
        msg = messages.get(r.status_code, f"API error {r.status_code}.")
        return {"error": f"{msg} (HTTP {r.status_code}) {detail}"}

    if r.status_code == 204 or not r.content:
        return {"ok": True}
    try:
        return r.json()
    except ValueError:
        return {"ok": True, "response": r.text[:300]}


@mcp.tool()
def list_posts(mine: bool = False) -> list | dict:
    """List posts on the Practice Hub.

    Set mine=True to return only the posts that belong to the token's owner.
    Use this first to discover post ids before reading, editing, or deleting.
    """
    return _request("GET", "/api/v1/posts", params={"mine": str(mine).lower()})


@mcp.tool()
def get_post(post_id: int) -> dict:
    """Fetch a single post by its numeric id, including title, body, and tags."""
    return _request("GET", f"/api/v1/posts/{post_id}")


@mcp.tool()
def create_post(title: str, body: str, tags: list[str] | None = None) -> dict:
    """Create a new post owned by the token's user.

    Args:
        title: The post title.
        body: The post body text.
        tags: Optional list of tag strings.
    """
    return _request(
        "POST", "/api/v1/posts",
        json={"title": title, "body": body, "tags": tags or []},
    )


@mcp.tool()
def update_post(
    post_id: int,
    title: str | None = None,
    body: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Edit one of your own posts. Only the fields you provide are changed.

    Returns a clear error if the post is not yours (403) or does not exist (404).
    """
    changes = {
        k: v for k, v in
        {"title": title, "body": body, "tags": tags}.items() if v is not None
    }
    if not changes:
        return {"error": "Nothing to update: provide title, body, or tags."}
    return _request("PATCH", f"/api/v1/posts/{post_id}", json=changes)


@mcp.tool()
def delete_post(post_id: int) -> dict:
    """Permanently delete one of your own posts by id.

    Returns a clear error if the post is not yours (403) or does not exist (404).
    """
    return _request("DELETE", f"/api/v1/posts/{post_id}")


if __name__ == "__main__":
    mcp.run()  # stdio transport
