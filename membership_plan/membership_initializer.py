from django.db import connection
from membership_plan.entity.membership import Membership

def table_exists(table_name: str) -> bool:
    with connection.cursor():
        return table_name in connection.introspection.table_names()

def create_default_memberships(sender, **kwargs):
    print("🚨 post_migrate 진입 시도됨!")

    if not table_exists("membership"):
        print("❌ membership 테이블이 아직 존재하지 않음. 초기화 중단")
        return

    default_memberships = [
        {"id": 1, "name": "하루 요금제", "price": 4000, "duration_days": 1, "plan_type": "DAY"},
        {"id": 2, "name": "일주일 요금제", "price": 20000, "duration_days": 7, "plan_type": "WEEK"},
        {"id": 3, "name": "한달 요금제", "price": 60000, "duration_days": 30, "plan_type": "MONTH"},
    ]

    for data in default_memberships:
        if not Membership.objects.filter(id=data["id"]).exists():
            Membership.objects.create(**data)
            print(f"✅ 요금제 생성됨: {data['name']}")
        else:
            print(f"🔁 이미 존재: {data['name']}")
