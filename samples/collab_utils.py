"""Utilities shared by the Google Colab samples."""

import hashlib
import os
import time
from typing import Any, Dict, List, Tuple


def try_add_user_secrets_to_env(userdata_keys: List[str]) -> None:
    """Load named Google Colab secrets into environment variables.

    Outside Google Colab, the function leaves the environment unchanged so the
    same examples can use environment variables supplied by another runtime.

    Args:
        userdata_keys: Secret names to load.
    """
    try:
        from google.colab import userdata
    except ImportError:
        return

    for key in userdata_keys:
        value = userdata.get(key)
        if value is None or not str(value).strip():
            raise RuntimeError(f"Google Colab secret {key} is empty.")
        os.environ[key] = str(value)

    print("Loaded Google Colab secrets: " + ", ".join(userdata_keys))


def try_add_optional_user_secrets_to_env(userdata_keys: List[str]) -> None:
    """Load Google Colab secrets that may not be configured."""
    try:
        from google.colab import userdata
    except ImportError:
        return

    loaded_keys = []
    for key in userdata_keys:
        try:
            value = userdata.get(key)
        except userdata.SecretNotFoundError:
            continue
        if value:
            os.environ[key] = str(value)
            loaded_keys.append(key)

    if loaded_keys:
        print("Loaded optional Google Colab secrets: " + ", ".join(loaded_keys))


def get_required_env(name: str) -> str:
    """Return a required environment variable with a helpful error message."""
    value = os.environ.get(name)
    if value is None or not value.strip():
        raise RuntimeError(
            f"{name} is required. Add it as a Google Colab secret or "
            "set it as an environment variable."
        )
    return value


def get_cid_for_bytes(data: bytes) -> str:
    """Return the vBase content identifier for an exact byte sequence."""
    return "0x" + hashlib.sha3_256(data).hexdigest()


def wait_for_stamp(
    client: Any,
    object_cid: str,
    collection_cid: str,
    *,
    filter_by_user: bool = False,
    user_address: str = None,
    timeout_seconds: int = 120,
    poll_interval_seconds: int = 5,
) -> Any:
    """Wait until a matching stamp is available through the verification API."""
    receipts = wait_for_stamps(
        client,
        [object_cid],
        collection_cid,
        filter_by_user=filter_by_user,
        user_address=user_address,
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    return receipts[object_cid.lower()]


def wait_for_stamps(
    client: Any,
    object_cids: List[str],
    collection_cid: str,
    *,
    filter_by_user: bool = False,
    user_address: str = None,
    timeout_seconds: int = 120,
    poll_interval_seconds: int = 5,
) -> Dict[str, Any]:
    """Wait until all requested stamps are available through verification."""
    deadline = time.monotonic() + timeout_seconds
    remaining = {object_cid.lower(): object_cid for object_cid in object_cids}
    receipts = {}

    while remaining and time.monotonic() < deadline:
        result = client.verify_stamps(
            list(remaining.values()),
            filter_by_user=filter_by_user,
        )
        for receipt in result.stamp_list:
            has_expected_stamp = (
                receipt.object_cid.lower() in remaining
                and receipt.set_cid.lower() == collection_cid.lower()
            )
            has_expected_user = (
                user_address is None
                or receipt.user_address.lower() == user_address.lower()
            )
            if has_expected_stamp and has_expected_user:
                normalized_cid = receipt.object_cid.lower()
                receipts[normalized_cid] = receipt
                remaining.pop(normalized_cid)

        if remaining:
            time.sleep(poll_interval_seconds)

    if not remaining:
        return receipts

    raise TimeoutError(
        "Timed out waiting for stamps to become available through the "
        "verification API: " + ", ".join(remaining.values())
    )


def create_s3_client_from_env() -> Any:
    """Create an S3 client using the standard AWS environment variables."""
    import boto3

    return boto3.client("s3")


def write_s3_object(
    s3_client: Any,
    bucket_name: str,
    prefix: str,
    file_name: str,
    data: bytes,
) -> str:
    """Write bytes to S3 and return the resulting object key."""
    object_key = f"{prefix.rstrip('/')}/{file_name}"
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    return object_key


def read_s3_objects(
    s3_client: Any, bucket_name: str, prefix: str
) -> List[Tuple[str, bytes]]:
    """Read all objects below an S3 prefix in stable key order."""
    normalized_prefix = prefix.rstrip("/") + "/"
    paginator = s3_client.get_paginator("list_objects_v2")
    object_keys = []

    for page in paginator.paginate(Bucket=bucket_name, Prefix=normalized_prefix):
        object_keys.extend(item["Key"] for item in page.get("Contents", []))

    objects = []
    for object_key in sorted(object_keys):
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        body = response["Body"]
        try:
            data = body.read()
        finally:
            close = getattr(body, "close", None)
            if close is not None:
                close()
        objects.append((object_key, data))
    return objects
