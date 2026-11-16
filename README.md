# Mini Project 7 - Practice Hub MCP Server

INF601 - Advanced Programming in Python - Khaleed Hossain

## What it does

`server.py` is a [Model Context Protocol](https://modelcontextprotocol.io) (MCP)
server built with **FastMCP** (official `mcp` Python SDK). It wraps the Practice
Hub REST API (`https://practice.fhsucyber.com`) so that Claude Code can read,
create, and modify *my* posts through natural-language requests.

It runs over the **stdio** transport (a local subprocess of Claude Code).

### Tools

| Tool | API call | Purpose |
|---|---|---|
| `list_posts(mine=False)` | `GET /api/v1/posts?mine=...` | List posts; `mine=True` for only my own |
| `get_post(post_id)` | `GET /api/v1/posts/{id}` | Fetch one post |
| `create_post(title, body, tags)` | `POST /api/v1/posts` | Create a post |
| `update_post(post_id, title?, body?, tags?)` | `PATCH /api/v1/posts/{id}` | Edit one of my posts (only given fields change) |
| `delete_post(post_id)` | `DELETE /api/v1/posts/{id}` | Delete one of my posts |

### Error handling

API failures never crash the server. Each tool returns `{"error": "..."}` with a
clear message instead:

- **401** - missing/invalid token (check `PRACTICE_API_TOKEN`)
- **403** - tried to edit/delete a post that isn't mine
- **404** - post id does not exist
- **422** - the API rejected the input
- Network errors/timeouts, and missing configuration, are also reported.

The server never prints to stdout (stdio carries the protocol); logs go to stderr.

## Install

Requires Python 3.10+.

```bash
git clone https://github.com/<your-username>/MiniProject7Khaleedhossain.git
cd MiniProject7Khaleedhossain
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

`requirements.txt` pins `mcp<2` because mcp 2.x renamed `FastMCP`.

## Configure environment variables

The token is read from the environment and is never stored in the code or repo.

```bash
export PRACTICE_API_URL="https://practice.fhsucyber.com"
```

(In PowerShell, set the URL with `$env:PRACTICE_API_URL = "https://practice.fhsucyber.com"`.)

Need a token? The API's `POST /api/v1/auth/token` endpoint accepts your email
and password and returns an `api_token`. Use the included helper to prompt for
credentials without saving them:

```bash
export PRACTICE_API_URL="https://practice.fhsucyber.com"
export PRACTICE_API_TOKEN="$(.venv/bin/python get_token.py)"
```

The password prompt is hidden, and the token is captured in the environment
rather than printed. To verify configuration without revealing the token:

```bash
python3 -c 'import os; print("URL set:", bool(os.getenv("PRACTICE_API_URL"))); print("Token set:", bool(os.getenv("PRACTICE_API_TOKEN")))'
```

## Quick check (optional)

`smoke_test.py` calls the tools directly: list, create, get, update, delete, and
a 404 case.

```bash
.venv/bin/python smoke_test.py
```

## Register with Claude Code

Run Claude Code from the same terminal where the environment variables are set.
Use absolute paths (replace `/absolute/path/to` with where you cloned the repo):

```bash
claude mcp add practice-hub -- \
  /absolute/path/to/MiniProject7Khaleedhossain/.venv/bin/python \
  /absolute/path/to/MiniProject7Khaleedhossain/server.py
```

Do not put the token directly in this command. If the server is already
registered, remove it before registering again: `claude mcp remove practice-hub`.

Confirm it registered and connected:

```bash
claude mcp list
```

## Run the acceptance test

Start Claude Code and ask:

> use the practice-hub tools to show my posts, create one, and edit its title.

Expected: Claude calls `list_posts` (mine), `create_post`, then `update_post`.
A transcript of my run is in [`acceptance_test/`](acceptance_test/).

## Files

- `server.py` - the MCP server
- `smoke_test.py` - direct tool check against the live API
- `requirements.txt` - dependencies
- `acceptance_test/` - Claude Code transcript/screenshots

## AI Usage

I used Claude Code (Anthropic) as a coding assistant for this project. It
helped draft `server.py`, `smoke_test.py`, `requirements.txt`, and this README
from the assignment requirements, and it found that `mcp` 2.x breaks the
`FastMCP` import (hence the `mcp<2` pin). I ran the smoke test against the live
API with my own token, ran the acceptance test in Claude Code myself, and
reviewed the code so I can explain how each tool, the error handling, and the
stdio transport work. My token was never committed to the repository.
