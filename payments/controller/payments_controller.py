from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status

from payments.service.payments_service_impl import PaymentsServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class PaymentsController(viewsets.ViewSet):
    redisCacheService = RedisCacheServiceImpl.getInstance()
    paymentsService = PaymentsServiceImpl.getInstance()

    def requestProcessPayments(self, request):
        print("🔥[1] 전체 요청 body:", request.data)
        postRequest = request.data
        userToken = postRequest.get("userToken")

        if not userToken:
            return JsonResponse({"error": "userToken이 필요합니다", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # userToken으로 계정 정보 조회
            accountId = self.redisCacheService.getValueByKey(userToken)
            print(f"🔑[2] userToken: {userToken} → accountId: {accountId}")
            if not accountId:
                return JsonResponse(
                    {"error": "유효하지 않은 userToken입니다", "success": False},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # paymentKey, orderId, amount와 같은 결제 정보 받아옴
            paymentKey = postRequest.get("paymentKey")
            orderId = postRequest.get("orderId")
            amount = postRequest.get("amount")
            orderInfoId = postRequest.get("orderInfoId")
            print(f"📦[3] paymentKey: {paymentKey}, orderId: {orderId}, amount: {amount}, orderInfoId: {orderInfoId}")

            if not paymentKey or not orderId or not amount or not orderInfoId:
                return JsonResponse(
                    {"error": "paymentKey, orderId, amount는 필수입니다.", "success": False},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 결제 처리
            print("⚙️[4] 결제 서비스 호출 전")
            paymentResult = self.paymentsService.process(accountId, paymentKey, orderId, amount, orderInfoId)
            print("✅[5] 결제 서비스 결과:", paymentResult)

            if paymentResult is not None and isinstance(paymentResult, dict):
                print("✅[6] 결제 성공 응답 구성 중")
                # 결제 성공 시 결제 URL과 ID 반환
                paymentUrl = paymentResult.get("receipt", {}).get("url", None)  # receipt URL을 받아옴
                paymentKey = paymentResult.get("paymentKey", None)  # paymentKey를 결제 KEY로 사용
                approvedAt = paymentResult.get("approvedAt")
                orderName = paymentResult.get("orderName")
                orderId = paymentResult.get("orderId")
                method = paymentResult.get("method")
                paymentAmount = paymentResult.get("easyPay", {}).get("amount")
                currency = paymentResult.get("currency", "KRW")

                if paymentUrl and paymentKey:
                    amountWithCurrency = f"{paymentAmount} {currency}"

                    return JsonResponse(
                        {
                            "success": True,
                            "message": "결제가 성공적으로 처리되었습니다.",
                            "paymentUrl": paymentUrl,  # 결제 URL
                            "paymentKey": paymentKey,  # 결제 KEY
                            "approvedAt": approvedAt,  # 결제 시간
                            "orderName": orderName,  # 구매 항목
                            "method": method,  # 결제 방법
                            "amountWithCurrency": amountWithCurrency,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return JsonResponse(
                        {"error": "결제 URL 또는 결제 ID를 찾을 수 없습니다", "success": False},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return JsonResponse(
                    {"error": "결제 처리 중 오류 발생", "success": False},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except Exception as e:
            # 서버 내부 오류 처리
            print(f"주문 처리 중 오류 발생: {e}")
            return JsonResponse(
                {"error": "서버 내부 오류", "success": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
