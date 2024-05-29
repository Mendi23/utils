import boto3

read_from_s3 = lambda client, bucket, key: client.get_object(
    Bucket=bucket, Key=key
    )['Body'].read().decode('utf-8')

write_to_s3 = lambda client, bucket, key, text: client.put_object(
    Body=text, Bucket=bucket, Key=key
    )

def get_s3_keys_with_prefix(s3_client: boto3.client, bucket: str, prefix: str):
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    for page in pages:
        yield from (r["Key"] for r in page['Contents'])
