from django.db import IntegrityError

from review.entity.review import Review
from review.repository.review_repository import ReviewRepository
from utility.s3_client import S3Client


class ReviewRepositoryImpl(ReviewRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def list(self, page, perPage):
        offset = (page - 1) * perPage
        reviewList = Review.objects.all().order_by('-create_date')[offset:offset + perPage]
        totalItems = Review.objects.count()

        return reviewList, totalItems

    def uploadToS3(self, fileContent: str, filename: str):
        try:
            s3Client = S3Client.getInstance()  # 싱글턴 인스턴스 사용
            s3Filename = f"review/{filename}"
            fileUrl = s3Client.upload_file(fileContent, s3Filename)  # 파일 업로드
            return filename

        except Exception as e:
            raise Exception(f"S3 업로드 실패: {str(e)}")

    def save(self, review: Review) -> Review:
        review.save()
        return review

    def findById(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    def deleteFromS3(self, filePath: str):
        try:
            s3Client = S3Client.getInstance()
            s3Client.deleteFile(filePath)
        except Exception as e:
            print(f"S3에서 파일 삭제 실패: {e}")

    def deleteById(self, id):
        try:
            # 게시글을 ID로 조회
            review = Review.objects.get(id=id)
            review.delete()  # 게시글 삭제
            return True  # 삭제 성공

        except Review.DoesNotExist:
            # 게시글이 존재하지 않으면 None을 반환
            print(f"게시글 ID {id}가 존재하지 않습니다.")
            return False  # 삭제 실패

        except IntegrityError as e:
            # 삭제 중에 발생한 예외 처리
            print(f"Error deleting board: {e}")
            return False  # 삭제 실패
