from abc import ABC, abstractmethod

# 유저별 구독 상태 관리용 인터페이스
class UserMembershipRepository(ABC):

    @abstractmethod
    def findByUserId(self, userId):
        # 특정 유저의 현재 구독 정보 조회
        pass

    @abstractmethod
    def save(self, userMembership):
        # 구독 정보 저장
        pass

    @abstractmethod
    def findExpiringWithinDays(self, days):
        # X일 내 만료되는 구독 리스트 조회 (자동 갱신 대상자 추출)
        pass

    @abstractmethod
    def findAllByUserId(self, userId):
        # 특정 유저의 모든 구독 이력
        pass

    @abstractmethod
    def countAll(self):
        pass

    @abstractmethod
    def countActive(self):
        pass

    @abstractmethod
    def totalRevenue(self):
        pass