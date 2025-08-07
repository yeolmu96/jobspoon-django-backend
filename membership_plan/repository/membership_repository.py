from abc import ABC, abstractmethod

# 구독 상품에 대한 데이터 접근 인터페이스
class MembershipRepository(ABC):

    @abstractmethod
    def findById(self, membershipId):
        # ID로 Membership 조회
        pass

    @abstractmethod
    def findAllActive(self):
        # 사용 가능한 모든 Membership 목록 조회
        pass

    @abstractmethod
    def save(self, membership):
        # Membership 저장 또는 수정
        pass