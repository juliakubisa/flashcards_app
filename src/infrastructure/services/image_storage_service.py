import boto3
from botocore.exceptions import ClientError


class ImageStorageService:
    bucket_name = 'flashcards-account-images'
    region_name = 'eu-north-1'

    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, url_age_seconds: int):
        self.url_age_seconds = url_age_seconds

        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=self.region_name
        )

        self.s3 = session.client('s3')

    def get_account_image_url(self, account_id: int) -> str | None:
        if self.__does_account_image_exists(account_id) == False:
            return None

        url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': str(account_id)},
            ExpiresIn=self.url_age_seconds
        )
        return url
    
    def __does_account_image_exists(self, account_id: int) -> bool:
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=str(account_id))
            return True
        except ClientError as error:
            if error.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                return False

