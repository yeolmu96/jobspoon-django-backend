from rest_framework import viewsets, status
from rest_framework.response import Response

from membership_plan.service.membership_service_impl import MembershipServiceImpl


class MembershipController(viewsets.ViewSet):
    membershipService = MembershipServiceImpl.getInstance()

    # ✅ 구독 생성
    def requestCreateMembership(self, request):
        user_id = request.data.get("userId")
        membership_id = request.data.get("membershipId")

        if not user_id or not membership_id:
            return Response({"error": "userId, membershipId는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_membership = self.membershipService.createMembership(user_id, membership_id)
            return Response({"message": "구독이 생성되었습니다.", "membershipId": user_membership.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ 유저 구독 상태 조회
    def requestGetUserMembership(self, request):
        user_id = request.query_params.get("userId")

        if not user_id:
            return Response({"error": "userId는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        user_membership = self.membershipService.getUserMembership(user_id)
        if not user_membership:
            return Response({"message": "구독 정보 없음"}, status=status.HTTP_204_NO_CONTENT)

        return Response({
            "membership": {
                "plan": user_membership.plan.name,
                "start_date": user_membership.start_date,
                "end_date": user_membership.end_date,
                "is_active": user_membership.is_active
            }
        }, status=status.HTTP_200_OK)

    # ✅ 구독 연장
    def requestExtendMembership(self, request):
        user_id = request.data.get("userId")
        days = request.data.get("days")

        if not user_id or not days:
            return Response({"error": "userId, days는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            extended = self.membershipService.extendMembership(user_id, int(days))
            return Response({"message": "구독이 연장되었습니다.", "new_end_date": extended.end_date}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ 만료 예정 구독 목록 조회
    def requestGetExpiringMemberships(self, request):
        days = request.query_params.get("days")
        if not days:
            return Response({"error": "days 파라미터는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        memberships = self.membershipService.getExpiringMemberships(int(days))
        data = [
            {
                "userId": m.user.id,
                "plan": m.plan.name,
                "end_date": m.end_date
            } for m in memberships
        ]
        return Response({"expiring_memberships": data}, status=status.HTTP_200_OK)

    # ✅ 자동 갱신 실행
    def requestRenewScheduledMemberships(self, request):
        try:
            count = self.membershipService.renewScheduledMemberships()
            return Response({"message": f"자동 갱신 완료: {count}건"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ 만료된 구독 비활성화
    def requestDeactivateExpiredMemberships(self, request):
        try:
            count = self.membershipService.deactivateExpiredMemberships()
            return Response({"message": f"비활성화 완료: {count}건"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestGetUserMembershipHistory(self, request):
        user_id = request.query_params.get("userId")
        if not user_id:
            return Response({"error": "userId는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        histories = self.membershipService.getUserMembershipHistory(user_id)
        data = [{
            "plan": h.plan.name,
            "start_date": h.start_date,
            "end_date": h.end_date,
            "is_active": h.is_active
        } for h in histories]
        return Response({"history": data}, status=status.HTTP_200_OK)

    def requestCancelMembership(self, request):
        user_id = request.data.get("userId")
        if not user_id:
            return Response({"error": "userId는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.membershipService.cancelMembership(user_id)
            return Response({"message": "구독이 취소되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestGetMembershipSummary(self, request):
        try:
            summary = self.membershipService.getMembershipSummary()
            return Response(summary, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
