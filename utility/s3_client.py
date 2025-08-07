import os
import boto3
from dotenv import load_dotenv

load_dotenv()  # .env 파일을 로드

class S3Client:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._initialize()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()  # 첫 호출 시 인스턴스를 생성
        return cls.__instance

    def _initialize(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')

    def upload_file(self, file_content: str, file_name: str) -> str:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=file_content,
                ContentType='text/html'
            )
            file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            return file_url
        except Exception as e:
            raise Exception(f"파일 업로드 실패: {str(e)}")

    def deleteFile(self, file_name: str):
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            print(f"파일 '{file_name}' 삭제 성공")
        except Exception as e:
            raise Exception(f"S3에서 파일 삭제 실패: {str(e)}")
