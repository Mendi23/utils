import os
import subprocess

import boto3

read_from_s3 = (
    lambda client, bucket, key: client.get_object(Bucket=bucket, Key=key)["Body"]
    .read()
    .decode("utf-8")
)

write_to_s3 = lambda client, bucket, key, text: client.put_object(
    Body=text, Bucket=bucket, Key=key
)


def get_s3_keys_with_prefix(s3_client: boto3.client, bucket: str, prefix: str):
    paginator = s3_client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    for page in pages:
        yield from (r["Key"] for r in page["Contents"])


def restore_deleted_s3_files(bucket: str, path_prefix: str, dry_run: bool = False):
    """
    Restore deleted files in an S3 path recursively by removing delete markers.

    Args:
        bucket: S3 bucket name
        path_prefix: Path prefix within the bucket to restore files from
        dry_run: If True, only print commands without executing them

    Returns:
        True if command executed successfully
    """
    cmd = (
        f"aws s3api list-object-versions --bucket {bucket} --prefix {path_prefix} "
        f"--output json --query 'DeleteMarkers[?IsLatest==`true`].[Key, VersionId]' | "
        f'jq -r \'.[] | "--key \\"" + .[0] + "\\" --version-id " + .[1]\''
        + f"| xargs -L1 -t aws s3api delete-object --bucket {bucket}"
    )

    print(f"Restoring deleted files in {path_prefix}")
    print(cmd)

    if not dry_run:
        exit_code = os.system(cmd)
        return exit_code == 0
    return True
