from django.db import models
from account.entity.account import Account
from membership_plan.entity.membership import Membership

# 실제 유저의 구독 상태를 나타내는 엔티티
class UserMembership(models.Model):
    # user ForeignKey를 IntegerField로 변경 (ORM 관계 제거)
    user_id = models.IntegerField()  # 구독 소유 유저 ID
    plan = models.ForeignKey(Membership, on_delete=models.PROTECT)  # 연결된 구독 상품
    start_date = models.DateTimeField(auto_now_add=True)  # 시작일
    end_date = models.DateTimeField()  # 만료일
    is_active = models.BooleanField(default=True)  # 현재 활성 상태 여부
    is_renew_scheduled = models.BooleanField(default=False)  # 자동 갱신 예약 여부

    # user 속성을 프로퍼티로 구현 (기존 코드와 호환성 유지)
    @property
    def user(self):
        """user_id를 통해 Account 객체를 필요할 때만 로드"""
        return Account.objects().get(id=self.user_id)
    
    @user.setter
    def user(self, user):
        """user 설정 시 user_id도 함께 설정"""
        if user is not None:
            self.user_id = user.id
        else:
            self.user_id = None

    class Meta:
        db_table = 'user_membership'

    def __str__(self):
        # 예: 'user123 - 프리미엄 (active)'
        user_str = f"User ID: {self.user_id}"
        try:
            user_obj = self.user
            user_str = str(user_obj)
        except Exception:
            pass
        return f"{user_str} - {self.plan} ({'active' if self.is_active else 'inactive'})"
