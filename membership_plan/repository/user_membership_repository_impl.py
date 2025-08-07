from datetime import timedelta
from django.utils import timezone

from membership_plan.entity.user_membership import UserMembership
from membership_plan.repository.user_membership_repository import UserMembershipRepository

# UserMembershipRepository 인터페이스의 구현체 (싱글톤 패턴 적용)
class UserMembershipRepositoryImpl(UserMembershipRepository):
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

    def findByUserId(self, userId):
        # 유저 ID 기준 가장 최근 구독 정보 1건 반환
        return UserMembership.objects.filter(user__id=userId).order_by('-end_date').first()

    def save(self, userMembership):
        userMembership.save()
        return userMembership

    def findExpiringWithinDays(self, days):
        # 현재 시점 기준 X일 내에 만료되는 구독 리스트 반환
        threshold_date = timezone.now() + timedelta(days=days)
        return UserMembership.objects.filter(end_date__lte=threshold_date, is_active=True)

    def findAllByUserId(self, userId):
        return UserMembership.objects.filter(user__id=userId).order_by('-start_date')

    def countAll(self):
        return UserMembership.objects.count()

    def countActive(self):
        return UserMembership.objects.filter(is_active=True).count()

    def totalRevenue(self):
        from django.db.models import Sum
        return UserMembership.objects.filter(is_active=True).aggregate(
            revenue=Sum('plan__price')
        )['revenue'] or 0