# GitHub Actions

## Policy
- Third-party actions are pinned by full commit SHA for reproducibility.
- Shared vBase-owned actions use `validityBase/vbase-github-actions` with reviewed release tags such as `@v1`.
- Workflow permissions are declared explicitly and kept minimal.
- Secrets must come from GitHub Secrets or deployment configuration, never from committed files, notebooks, screenshots, or logs.

## Workflows

### `.github/workflows/update-main-docs.yml`
- Runs on pushes to `main` and manual dispatch.
- Checks out the repository with the pinned `actions/checkout` action.
- Publishes the committed Markdown files from `docs/`.
- Uses `validityBase/vbase-github-actions/.github/actions/publish-docs@v1`.
- Publishes to the `main` branch of the central docs repository.
- Uses `DOCS_REPO_ACCESS_TOKEN` for the central docs repository.

### `.github/workflows/python-dependency-locks.yml`
- Runs on pull requests that modify Python dependency inputs, generated locks, or helper modules.
- Uses `validityBase/vbase-github-actions/.github/actions/setup-python-deps@v1`.
- Regenerates sample and lock-tooling requirement locks with hashes.
- Installs generated locks with `require-hashes: "true"`, runs `pip check`, and compiles `samples/collab_utils.py`.
