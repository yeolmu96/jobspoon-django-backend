import uuid

from account.repository.account_repository_impl import AccountRepositoryImpl
from account_profile.repository.account_profile_repository_impl import AccountProfileRepositoryImpl
from review.entity.review import Review
from review.repository.review_repository_impl import ReviewRepositoryImpl
from review.service.review_service import ReviewService


class ReviewServiceImpl(ReviewService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__reviewRepository = ReviewRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__accountProfileRepository = AccountProfileRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestList(self, page, perPage):
        paginatedReviewList, totalItems = self.__reviewRepository.list(page, perPage)

        totalPages = (totalItems + perPage - 1) // perPage

        paginatedFilteringReviewList = [
            {
                "id": review.id,
                "title": review.title,
                "nickname": review.writer.email,  # writer 객체의 nickname 가져오기
                "createDate": review.create_date.strftime("%Y-%m-%d %H:%M"),
            }
            for review in paginatedReviewList
        ]

        print(f"paginatedFilteringReviewList: {paginatedFilteringReviewList}")

        return paginatedFilteringReviewList, totalItems, totalPages

    def requestUploadToS3(self, file, title):
        filename = f"{title}-{uuid.uuid4()}.html"

        print(f"filename: {filename}")

        return self.__reviewRepository.uploadToS3(file, filename)

    def requestCreate(self, title, content, accountId):
        if not title or not content:
            raise ValueError("Title and content are required fields.")
        if not accountId:
            raise ValueError("Account ID is required.")

            # 2. Account 조회
        account = self.__accountRepository.findById(accountId)
        if not account:
            raise ValueError(f"Account with ID {accountId} does not exist.")

        # 4. Board 객체 생성 및 저장
        review = Review(
            title=title,
            content=content,
            writer=account)  # ForeignKey로 연결된 account_profile)
        savedReview = self.__reviewRepository.save(review)

        # 5. 응답 데이터 구조화
        return {
            "id": savedReview.id,
            "title": savedReview.title,
            "content": review.content,
            "writerNickname": savedReview.writer.email,
            "createDate": savedReview.create_date.strftime("%Y-%m-%d %H:%M"),
        }

    def requestRead(self, id):
        review = self.__reviewRepository.findById(id)
        if review:
            return {
                "id": review.id,
                "title": review.title,
                "content": review.content,
                "createDate": review.create_date.strftime("%Y-%m-%d %H:%M"),
                "nickname": review.writer.email
            }

        return None

    def requestUpdate(self, id, title, accountId):
        try:
            account = self.__accountRepository.findById(accountId)

            review = self.__reviewRepository.findById(id)

            # 게시글 작성자와 요청한 사용자가 동일한지 확인
            if review.writer.id != account.id:
                raise ValueError("You are not authorized to modify this post.")

            # 제목 업데이트
            review.title = title

            # 게시글 저장 (수정)
            updatedReview = self.__reviewRepository.save(review)

            # 수정된 게시글 반환
            return {
                "id": updatedReview.id,
                "title": updatedReview.title,
                "content": updatedReview.content,
                "writerNickname": updatedReview.writer.email,  # 작성자의 닉네임
                "createDate": updatedReview.create_date.strftime("%Y-%m-%d %H:%M"),
            }

        except Review.DoesNotExist:
            raise ValueError(f"BlogPost with ID {updatedReview} does not exist.")
        except Exception as e:
            raise Exception(f"Error while modifying the post: {str(e)}")

    def requestDelete(self, id, accountId):
        try:
            account = self.__accountRepository.findById(accountId)
            #accountProfile = self.__accountProfileRepository.findByAccount(account)

            review = self.__reviewRepository.findById(id)
            if not review:
                raise ValueError(f"Review with ID {id} does not exist.")

            if review.writer.id != account.id:
                raise ValueError("You are not authorized to modify this post.")

            content = f"review/{review.content}"
            self.__reviewRepository.deleteFromS3(content)

            # 게시글 삭제 요청
            success = self.__reviewRepository.deleteById(id)
            return success

        except Exception as e:
            raise Exception(f"게시글 삭제 중 오류 발생: {str(e)}")
