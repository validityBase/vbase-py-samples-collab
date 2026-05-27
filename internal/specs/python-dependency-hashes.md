# Python Dependency Hashes

Python dependencies use pip-tools input files plus generated hash-locked output
files.

## Pattern

- Human-edited inputs live in `requirements.in` files.
- Generated locks live in matching `requirements.txt` files and include
  `--hash` entries.
- Install generated locks with `python -m pip install --require-hashes -r <file>`.
- Do not edit generated lock files by hand.
- The public vBase SDK dependency is `vbase==1.0.0`.

## Files

- `requirements.in` -> `requirements.txt`: sample notebook dependencies.
- `requirements-lock.in` -> `requirements-lock.txt`: pinned pip-tools setup.

## Regeneration

Use the pinned lock tooling:

```bash
python -m pip install --require-hashes -r requirements-lock.txt
```

Regenerate locks with the Python version used by
`.github/workflows/python-dependency-locks.yml`:

```bash
pip-compile --strip-extras --no-annotate --generate-hashes -o requirements.txt requirements.in
pip-compile --strip-extras --no-annotate --allow-unsafe --generate-hashes -o requirements-lock.txt requirements-lock.in
```
