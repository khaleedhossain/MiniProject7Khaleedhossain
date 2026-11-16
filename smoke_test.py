# INF601 - Advanced Programming in Python
# Khaleed Hossain
# Mini Project 7
"""Quick check of the five tools against the live API (uses your env vars).

Run: .venv/bin/python smoke_test.py
Creates one post, edits it, then deletes it. Prints no token.
"""

import server


def show(label, result):
    print(f"\n== {label} ==\n{result}")
    return result


mine = show("list_posts(mine=True)", server.list_posts(mine=True))
created = show("create_post", server.create_post("MCP smoke test", "hello", ["test"]))
pid = created.get("id") if isinstance(created, dict) else None
if pid is not None:
    show("get_post", server.get_post(pid))
    show("update_post", server.update_post(pid, title="MCP smoke test (edited)"))
    show("delete_post", server.delete_post(pid))
    show("get_post after delete (expect 404 message)", server.get_post(pid))
show("get_post(999999999) (expect 404 message)", server.get_post(999999999))
