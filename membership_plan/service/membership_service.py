from abc import ABC, abstractmethod

# 구독 관련 비즈니스 로직 인터페이스
class MembershipService(ABC):

    @abstractmethod
    def createMembership(self, userId, membershipId):
        # 유저가 특정 멤버십을 구독 시작
        pass

    @abstractmethod
    def getUserMembership(self, userId):
        # 현재 유저의 구독 상태 조회
        pass

    @abstractmethod
    def extendMembership(self, userId, days):
        # 구독 연장 (예: 자동 갱신 또는 수동 연장)
        pass

    @abstractmethod
    def getExpiringMemberships(self, withinDays):
        # N일 이내 만료될 유저 구독 목록 조회 (자동 갱신용)
        pass

    @abstractmethod
    def renewScheduledMemberships(self):
        # 자동 갱신 대상인 유저의 구독을 현재 시점 기준으로 새 기간으로 연장
        pass

    @abstractmethod
    def deactivateExpiredMemberships(self):
        # 이미 만료된 구독을 찾아 is_active=False로 비활성화
        pass

    @abstractmethod
    def getUserMembershipHistory(self, userId):
        pass

    @abstractmethod
    def cancelMembership(self, userId):
        pass

    @abstractmethod
    def getMembershipSummary(self):
        pass