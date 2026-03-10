import boto3
import dlt

s3 = boto3.client(
    "s3",
    aws_access_key_id=dlt.secrets["destination.filesystem.credentials.aws_access_key_id"],
    aws_secret_access_key=dlt.secrets["destination.filesystem.credentials.aws_secret_access_key"],
)

response = s3.list_objects_v2(
    Bucket='gtm-demos',
    Prefix='snowflake-demo/'
)

print("Files in S3 staging:")
for obj in response.get('Contents', []):
    print(obj['Key']) 