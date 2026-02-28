import os
import cuid
import boto3

S3 = None

def get_client():
    global S3
    if S3 is None:
        S3 = boto3.client(
            "s3",
            endpoint_url=f"https://{os.environ.get('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            aws_access_key_id=os.environ.get('R2_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('R2_SECRET_ACCESS_KEY'),
            region_name="auto"
        )
    return S3

def upload_markup(markup, bucket_name):
    cuid_str = cuid.cuid()

    get_client().put_object(
        Body = markup.encode('utf-8'),
        Bucket = bucket_name,
        Key = cuid_str,
        ContentType = "image/svg+xml",
    )

    return cuid_str

def get_object_url(file_key, bucket_name, public_domain=None):
    if public_domain:
        return f"{public_domain.rstrip('/')}/{file_key}"
    
    try:
        get_client().get_object(
            Key=file_key,
            Bucket=bucket_name
        )

    except(Exception):
        return None

    return get_client().generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket_name, "Key": file_key},
    ).split("?")[0]

def upload_file(
    local_file_path,
    bucket_name,
    file_key,
    public_domain=None
):
    get_client().upload_file(
        local_file_path,
        bucket_name,
        file_key,
    )
    return get_object_url(file_key, bucket_name, public_domain)
