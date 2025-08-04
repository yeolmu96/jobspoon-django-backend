from membership_plan.entity.membership import Membership
from membership_plan.repository.membership_repository import MembershipRepository

# MembershipRepository 인터페이스의 실제 구현체 (싱글톤 패턴 적용)
class MembershipRepositoryImpl(MembershipRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        # 싱글톤 인스턴스 반환
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def findById(self, membershipId):
        try:
            return Membership.objects.get(id=membershipId)
        except Membership.DoesNotExist:
            return None

    def findAllActive(self):
        return Membership.objects.filter(is_active=True)

    def save(self, membership):
        membership.save()
        return membership