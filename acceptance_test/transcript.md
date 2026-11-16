# Acceptance test transcript

The following results were provided from a Claude Code run using the
`practice-hub` MCP server against the live Practice Hub API.

## 1. List my posts

Request: `list_posts(mine=True)`

```json
{"result": []}
```

There were no existing posts.

## 2. Create a test post

Request: `create_post`

```json
{
  "id": 67,
  "title": "Mini Project 7 Test Post",
  "body": "This is a test post created for Mini Project 7 (INF601G) via the Practice Hub MCP tools.",
  "tags": ["mini-project-7", "test"],
  "author_id": 18,
  "author_name": "Khaleed hossain",
  "created_at": "2026-11-16T19:29:49.290640",
  "updated_at": "2026-11-16T19:29:49.290651",
  "attachments": []
}
```

## 3. Update the post title

Request: `update_post(post_id=67, title="Mini Project 7 Test Post (Updated Title)")`

```json
{
  "id": 67,
  "title": "Mini Project 7 Test Post (Updated Title)",
  "body": "This is a test post created for Mini Project 7 (INF601G) via the Practice Hub MCP tools.",
  "tags": ["mini-project-7", "test"],
  "author_id": 18,
  "author_name": "Khaleed hossain",
  "created_at": "2026-11-16T19:29:49.290640",
  "updated_at": "2026-11-16T19:29:50.594969",
  "attachments": []
}
```

The title changed and `updated_at` advanced; the body and tags remained unchanged.
The test post was left on Practice Hub.
