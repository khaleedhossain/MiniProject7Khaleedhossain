# INF601 - Advanced Programming in Python
# Khaleed Hossain
# Mini Project 7
"""Request a Practice Hub API token without saving account credentials."""

import getpass
import os
import sys

import httpx


DEFAULT_API_URL = "https://practice.fhsucyber.com"


def request_token(base_url: str, email: str, password: str) -> str:
    """Request and return an API token using the documented email/password endpoint."""
    response = httpx.post(
        f"{base_url.rstrip('/')}/api/v1/auth/token",
        json={"email": email, "password": password},
        timeout=15.0,
    )
    if response.is_error:
        try:
            error_payload = response.json()
        except ValueError:
            error_payload = None
        detail = (
            error_payload.get("detail", response.text[:300])
            if isinstance(error_payload, dict)
            else response.text[:300]
        )
        raise RuntimeError(f"Token request failed (HTTP {response.status_code}): {detail}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise RuntimeError("Token endpoint returned invalid JSON.") from exc

    token = payload.get("api_token") if isinstance(payload, dict) else None
    if not isinstance(token, str) or not token.strip():
        raise RuntimeError("Token endpoint response did not contain an api_token.")
    return token


def main() -> int:
    base_url = os.environ.get("PRACTICE_API_URL", DEFAULT_API_URL).rstrip("/")
    print("Practice Hub email: ", end="", file=sys.stderr, flush=True)
    email = input().strip()
    password = getpass.getpass("Practice Hub password: ")

    try:
        token = request_token(base_url, email, password)
    except (httpx.HTTPError, RuntimeError) as exc:
        print(f"Could not get a Practice Hub token: {exc}", file=sys.stderr)
        return 1

    # Keep stdout machine-readable so the token can be captured without displaying it.
    print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
