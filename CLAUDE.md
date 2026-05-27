# CLAUDE.md

This repository contains vBase Python sample notebooks for Google Colab.

## Core Standards

- Keep notebooks focused on clear, runnable sample flows.
- Do not commit secrets, private keys, API tokens, `.env` files, or notebook
  outputs containing credentials.
- Runtime dependencies are declared in `requirements.in`; generated lock files
  are committed with hashes and must not be edited by hand.
- Documents published externally live in `docs/`.
- Internal specs, guides, and agent memory live in `internal/`.

## Internal Documentation

- Agent memory: [internal/agents/memory/MEMORY.md](internal/agents/memory/MEMORY.md)
- GitHub Actions: [internal/specs/github-actions.md](internal/specs/github-actions.md)
- Python dependency hashes: [internal/specs/python-dependency-hashes.md](internal/specs/python-dependency-hashes.md)
