"""Structural and syntax checks for the public Google Colab samples."""

import ast
import json
import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((REPOSITORY_ROOT / "samples").glob("*.ipynb"))
EXPECTED_NOTEBOOK_NAMES = {
    "add_string_dataset_record.ipynb",
    "add_string_dataset_record_async.ipynb",
    "create_set.ipynb",
    "produce_portfolio_history_s3.ipynb",
    "produce_sentiment_dataset_history_s3.ipynb",
    "setup.ipynb",
    "verify_portfolio_history_s3.ipynb",
    "verify_sentiment_dataset_history_s3.ipynb",
}
PUBLIC_CONTENT_FILES = NOTEBOOKS + [
    REPOSITORY_ROOT / "README.md",
    REPOSITORY_ROOT / "docs" / "quickstart.md",
    REPOSITORY_ROOT / "samples" / "collab_utils.py",
]

LEGACY_OR_INTERNAL_MARKERS = (
    "from vbase import",
    "VBASE_FORWARDER_URL",
    "VBASE_COMMITMENT_SERVICE_PRIVATE_KEY",
    "ForwarderCommitmentService",
    "VBaseDataset",
)


def get_python_source(cell):
    """Remove IPython magic and shell lines before compiling a code cell."""
    source_lines = []
    for line in cell.get("source", []):
        if line.lstrip().startswith(("%", "!")):
            continue
        source_lines.append(line)
    return "".join(source_lines)


class NotebookTests(unittest.TestCase):
    """Keep every published notebook clean and syntactically valid."""

    def test_expected_notebooks_are_present(self):
        self.assertEqual({path.name for path in NOTEBOOKS}, EXPECTED_NOTEBOOK_NAMES)

    def test_notebook_code_cells_compile(self):
        for notebook_path in NOTEBOOKS:
            with self.subTest(notebook=notebook_path.name):
                notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
                for cell_number, cell in enumerate(notebook["cells"], start=1):
                    if cell["cell_type"] != "code":
                        continue
                    source = get_python_source(cell)
                    compile(
                        source,
                        f"{notebook_path.name}:cell-{cell_number}",
                        "exec",
                        flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
                    )

    def test_notebooks_have_no_saved_execution_state(self):
        for notebook_path in NOTEBOOKS:
            with self.subTest(notebook=notebook_path.name):
                notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
                for cell in notebook["cells"]:
                    if cell["cell_type"] != "code":
                        continue
                    self.assertIsNone(cell.get("execution_count"))
                    self.assertEqual(cell.get("outputs", []), [])

    def test_notebooks_do_not_reference_legacy_or_internal_configuration(self):
        for notebook_path in NOTEBOOKS:
            with self.subTest(notebook=notebook_path.name):
                notebook_text = notebook_path.read_text(encoding="utf-8")
                for marker in LEGACY_OR_INTERNAL_MARKERS:
                    self.assertNotIn(marker, notebook_text)
                self.assertIsNone(
                    re.search(r"\b[A-Z]{2,10}-\d+\b", notebook_text),
                    notebook_path.name,
                )

    def test_public_content_does_not_reference_internal_task_ids(self):
        for content_path in PUBLIC_CONTENT_FILES:
            with self.subTest(path=content_path.relative_to(REPOSITORY_ROOT)):
                content = content_path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"\b[A-Z]{2,10}-\d+\b", content))


if __name__ == "__main__":
    unittest.main()
