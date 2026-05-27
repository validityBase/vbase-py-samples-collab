# Agent Memory

## GitHub Actions
- Third-party GitHub Actions are pinned to full commit SHAs.
- vBase-owned shared actions use reviewed `validityBase/vbase-github-actions` version tags.
- Documentation publishing uses `validityBase/vbase-github-actions/.github/actions/publish-docs@v1`.
- Docs are already committed as Markdown in `docs/`, so docs publishing does not need Python setup or Sphinx build steps.
- Docs publishing targets the `main` branch of the central docs repository.

## Python Dependencies
- Sample dependencies are declared in `requirements.in`; generated `requirements.txt` includes pinned versions and hashes.
- Install generated lock files with `python -m pip install --require-hashes -r <file>`.
- `requirements-lock.txt` pins pip-tools for lock regeneration.
- The public vBase SDK dependency is installed from PyPI as `vbase==1.0.0`.
