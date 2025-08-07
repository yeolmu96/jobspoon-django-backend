from django.http import JsonResponse
from rest_framework import viewsets, status

from account_profile.entity.account_profile import AccountProfile
from account_profile.service.account_profile_service_impl import AccountProfileServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class AccountProfileController(viewsets.ViewSet):
    __accountProfileService = AccountProfileServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestInfo(self, request):
        postRequest = request.data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        userToken = postRequest.get("userToken")
        print(f"인포용 userToken: {userToken}")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다"}, status=400)
        try:
            accountId = self.redisCacheService.getValueByKey(userToken)
            if not accountId:
                return JsonResponse({"error": "유효하지 않은 userToken입니다"}, status=404)

            # 서비스에서 데이터 가져오기
            foundEmail = self.__accountProfileService.findEmail(accountId)
            #foundRoleType = self.__accountProfileService.findRoleType(accountId)
            foundNickName = self.__accountProfileService.findNickname(accountId)
            foundGender = self.__accountProfileService.findGender(accountId)
            foundBirthyear = self.__accountProfileService.findBirthyear(accountId)

            return JsonResponse({
                "email": foundEmail,
               # "roleType": foundRoleType,
                "nickname": foundNickName,
                "gender": foundGender,
                "birthyear": foundBirthyear,
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)





    '''''
    def request_info(self, request):
        # 인증된 사용자를 가져옵니다.
        user = request.user
        try:
            profile = AccountProfile.objects.get(account=user)
            print(f"DB에서 발견한 profile: {profile}")
        except AccountProfile.DoesNotExist:
            print("AccountProfile DB에서 정보 못찾음")
            return JsonResponse({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            "email": profile.email,
            "nickname": profile.nickname,
            "gender": profile.gender,
            "birthyear": profile.birthyear,
        }, status=status.HTTP_200_OK)
'''