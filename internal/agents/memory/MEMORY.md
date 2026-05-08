# Agent Memory

## GitHub Actions
- Third-party GitHub Actions are pinned to full commit SHAs.
- vBase-owned shared actions use reviewed `validityBase/vbase-github-actions` version tags.
- Documentation publishing uses `validityBase/vbase-github-actions/.github/actions/publish-docs@v1`.
- Docs are already committed as Markdown in `docs/`, so docs publishing does not need Python setup or Sphinx build steps.
- Docs publishing targets the `main` branch of the central docs repository.
