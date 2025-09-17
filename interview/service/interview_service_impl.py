from account.repository.account_repository_impl import AccountRepositoryImpl
from interview.entity.interview import Interview
from interview.entity.interview_answer import InterviewAnswer
from interview.entity.interview_status import InterviewStatus
from interview.repository.interview_answer_repository_impl import InterviewAnswerRepositoryImpl
from interview.repository.interview_repository_impl import InterviewRepositoryImpl
from interview.service.interview_service import InterviewService


class InterviewServiceImpl(InterviewService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__interviewRepository = InterviewRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__interviewAnswerRepository = InterviewAnswerRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    # 인터뷰 생성
    def createInterview(
        self,
        accountId,
        jobCategory,
        experienceLevel,
        projectExperience,
        academicBackground,
        techStack,
        companyName
    ):
        foundAccount = self.__accountRepository.findById(accountId)
        print(f"인터뷰 생성 서비스 계층 진입")

        if not foundAccount:
            raise Exception("해당 accountId에 해당하는 account를 찾을 수 없습니다.")

        # ✅ techStack이 필수
        if not techStack or not isinstance(techStack, list) or len(techStack) == 0:
            raise ValueError("techStack은 비어 있을 수 없습니다.")

        newInterview = Interview(
            account=foundAccount,
            status=InterviewStatus.IN_PROGRESS.value,
            topic=jobCategory.value if hasattr(jobCategory, 'value') else jobCategory,
            experience_level=experienceLevel.value if hasattr(experienceLevel, 'value') else experienceLevel,
            project_experience=projectExperience.value if hasattr(projectExperience, 'value') else projectExperience,
            academic_background=academicBackground.value if hasattr(academicBackground, 'value') else academicBackground,
            tech_stack=techStack,
            company_name=companyName.value if hasattr(companyName, 'value') else companyName
        )
        print(f"newInterview: {newInterview}")

        savedInterview = self.__interviewRepository.save(newInterview)
        return savedInterview

    # 질문 저장
    def saveQuestion(self, interview_id: int, question: str) -> int | None:
        print(f"📥 [service] Saving question to DB for interviewId={interview_id}")
        return self.__interviewRepository.saveQuestion(interview_id, question)

    # 인터뷰 목록 조회
    def listInterview(self, accountId, page, pageSize):
        try:
            account = self.__accountRepository.findById(accountId)
            if not account:
                raise ValueError(f"Account with ID {accountId} not found.")

            paginatedInterviewList = self.__interviewRepository.findInterviewByAccount(accountId, page, pageSize)
            total_items = paginatedInterviewList.paginator.count

            interviewDataList = [
                {
                    "id": interview.id,
                    "topic": interview.topic,
                    "created_at": interview.created_at,
                    "status": interview.status,  # ✅ 추가
                    # "yearsOfExperience": interview.experience_level
                }
                for interview in paginatedInterviewList
            ]

            return interviewDataList, total_items

        except Exception as e:
            print(f"Unexpected error in listInterview: {e}")
            raise

    # 인터뷰 삭제
    def removeInterview(self, accountId, interviewId):
        try:
            interview = self.__interviewRepository.findById(interviewId)
            if interview is None or str(interview.account_id) != str(accountId):
                return {
                    "error": "해당 인터뷰를 찾을 수 없거나 소유자가 일치하지 않습니다.",
                    "success": False
                }

            result = self.__interviewRepository.deleteById(interviewId)
            if result:
                return {"success": True, "message": "인터뷰가 삭제되었습니다."}

        except Exception as e:
            print(f"Error in InterviewService.removeInterview: {e}")
            return {"error": "서버 내부 오류", "success": False}

    # 답변 저장
    def saveAnswer(self, accountId: int, interviewId: int, questionId: int, answerText: str) -> bool:
        try:
            interviewAnswer = InterviewAnswer(
                account_id=accountId,
                interview_id=interviewId,
                question_id=questionId,
                answer_text=answerText
            )
            result = self.__interviewAnswerRepository.save(interviewAnswer)
            return result is not None
        except Exception as e:
            print(f"답변 저장 중 오류 발생: {e}")
            return False
