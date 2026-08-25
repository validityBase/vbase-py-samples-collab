"""Tests for helpers shared by the Google Colab samples."""

import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SAMPLES_DIR = Path(__file__).resolve().parents[1] / "samples"
sys.path.insert(0, str(SAMPLES_DIR))

from collab_utils import (  # noqa: E402
    get_cid_for_bytes,
    get_required_env,
    read_s3_objects,
    wait_for_stamps,
    write_s3_object,
)


class FakePaginator:
    """Return configured S3 listing pages."""

    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def paginate(self, **kwargs):
        self.calls.append(kwargs)
        return self.pages


class FakeS3Client:
    """Provide the S3 methods used by the sample helpers."""

    def __init__(self):
        self.paginator = FakePaginator(
            [
                {
                    "Contents": [
                        {"Key": "records/b.json"},
                        {"Key": "records/a.json"},
                    ]
                }
            ]
        )
        self.payloads = {
            "records/a.json": b"a",
            "records/b.json": b"b",
        }
        self.put_calls = []

    def get_paginator(self, operation_name):
        if operation_name != "list_objects_v2":
            raise AssertionError(f"Unexpected operation: {operation_name}")
        return self.paginator

    def get_object(self, *, Bucket, Key):
        del Bucket
        return {"Body": SimpleNamespace(read=lambda: self.payloads[Key])}

    def put_object(self, **kwargs):
        self.put_calls.append(kwargs)


class FakeVBaseClient:
    """Return a fixed set of verification receipts."""

    def __init__(self, receipts):
        self.receipts = receipts
        self.calls = []

    def verify_stamps(self, object_cids, filter_by_user=False):
        self.calls.append((object_cids, filter_by_user))
        return SimpleNamespace(stamp_list=self.receipts)


class ColabUtilsTests(unittest.TestCase):
    """Verify deterministic hashing, storage, and receipt matching."""

    def test_get_cid_for_bytes_uses_sha3_256(self):
        self.assertEqual(
            get_cid_for_bytes(b"hello"),
            "0x3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392",
        )

    def test_get_required_env_rejects_missing_and_empty_values(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "VBASE_API_KEY is required"):
                get_required_env("VBASE_API_KEY")

        with patch.dict(os.environ, {"VBASE_API_KEY": ""}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "VBASE_API_KEY is required"):
                get_required_env("VBASE_API_KEY")

        with patch.dict(os.environ, {"VBASE_API_KEY": "   "}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "VBASE_API_KEY is required"):
                get_required_env("VBASE_API_KEY")

    def test_s3_helpers_write_bytes_and_read_objects_in_key_order(self):
        client = FakeS3Client()

        object_key = write_s3_object(
            client,
            "sample-bucket",
            "records/",
            "c.json",
            b"c",
        )
        objects = read_s3_objects(client, "sample-bucket", "records")

        self.assertEqual(object_key, "records/c.json")
        self.assertEqual(
            client.put_calls,
            [
                {
                    "Bucket": "sample-bucket",
                    "Key": "records/c.json",
                    "Body": b"c",
                }
            ],
        )
        self.assertEqual(objects, [("records/a.json", b"a"), ("records/b.json", b"b")])
        self.assertEqual(
            client.paginator.calls,
            [{"Bucket": "sample-bucket", "Prefix": "records/"}],
        )

    def test_wait_for_stamps_requires_the_expected_collection_and_owner(self):
        receipts = [
            SimpleNamespace(
                object_cid="0xaaa",
                set_cid="0xwrong",
                user_address="0xowner",
            ),
            SimpleNamespace(
                object_cid="0xaaa",
                set_cid="0xcollection",
                user_address="0xowner",
            ),
            SimpleNamespace(
                object_cid="0xbbb",
                set_cid="0xcollection",
                user_address="0xwrong",
            ),
            SimpleNamespace(
                object_cid="0xbbb",
                set_cid="0xcollection",
                user_address="0xowner",
            ),
        ]
        client = FakeVBaseClient(receipts)

        matches = wait_for_stamps(
            client,
            ["0xaaa", "0xbbb"],
            "0xcollection",
            user_address="0xowner",
            timeout_seconds=1,
            poll_interval_seconds=0,
        )

        self.assertEqual(set(matches), {"0xaaa", "0xbbb"})
        self.assertEqual(client.calls, [(["0xaaa", "0xbbb"], False)])


if __name__ == "__main__":
    unittest.main()
