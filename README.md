# AgentLens

Run, trace and evaluate AI agents. See every step an agent takes (prompt, tool
call, tokens, latency, cost) and catch regressions when a prompt changes.

## Development

    cd backend
    uv sync
    uv run pytest
    uv run ruff check . && uv run ruff format --check . && uv run mypy app

Install the git hooks once:

    cd backend && uv run pre-commit install --config ../.pre-commit-config.yaml

CI runs the same checks (lint, format, mypy strict, tests) plus a Docker build
on every pull request.
