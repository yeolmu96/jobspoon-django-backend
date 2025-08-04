import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from review.service.review_service_impl import ReviewServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class ReviewController(viewsets.ViewSet):
    reviewService = ReviewServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestReviewList(self, request):
        getRequest = request.GET
        page = int(getRequest.get("page", 1))
        perPage = int(getRequest.get("perPage", 8))
        paginatedReview, totalItems, totalPages = self.reviewService.requestList(page, perPage)

        # JSON 응답 생성
        return JsonResponse({
            "dataList": paginatedReview,  # 게시글 정보 목록
            "totalItems": totalItems,  # 전체 게시글 수
            "totalPages": totalPages  # 전체 페이지 수
        }, status=status.HTTP_200_OK)

    def requestUploadReview(self, request):
        fileContent = request.data.get('content')
        if not fileContent:
            return JsonResponse({'error': '파일을 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"fileContent: {fileContent}")
        title = request.data.get('title')

        try:
            filename = self.reviewService.requestUploadToS3(fileContent, title)
            return JsonResponse({'filename': filename}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': f'오류 발생: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestCreateReview(self, request):
        postRequest = request.data
        print("📥 받은 데이터:", postRequest)

        title = postRequest.get("title")
        content = postRequest.get("content")
        imageUrl = postRequest.get("imageUrl")
        userToken = postRequest.get("userToken")

        if not userToken:  # userToken이 없거나 빈 문자열이면 400 반환
            return JsonResponse(
                {"error": "User token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        accountId = self.redisCacheService.getValueByKey(userToken)
        print(f'requestCreateBlogPost() accountId: ${accountId}')

        if not accountId:  # userToken이 유효하지 않은 경우도 거부
            return JsonResponse(
                {"error": "Invalid user token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        savedReview = self.reviewService.requestCreate(title, content, accountId)

        return JsonResponse({"data": savedReview}, status=status.HTTP_200_OK)

    def requestReadReview(self, request, pk=None):
        try:
            if not pk:
                return JsonResponse({"error": "ID를 제공해야 합니다."}, status=400)

            print(f"requestReadReview() -> pk: {pk}")
            readReview = self.reviewService.requestRead(pk)
            print("readReview:", readReview)

            return JsonResponse(readReview, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def requestUpdateReview(self, request, pk=None):
        try:
            postRequest = request.data
            print(f"postRequest: {postRequest}")

            title = postRequest.get("title")

            # 필수 항목 체크
            if not title:
                return JsonResponse({"error": "Title are required."}, status=status.HTTP_400_BAD_REQUEST)

            userToken = postRequest.get("userToken")
            accountId = self.redisCacheService.getValueByKey(userToken)

            # 게시글 수정 요청 처리
            updatedReview = self.reviewService.requestUpdate(pk, title, accountId)

            return JsonResponse(updatedReview, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def requestDeleteReview(self, request, pk=None):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({"error": "인증 토큰이 없습니다."}, status=401)

            userToken = auth_header.split("Bearer ")[1]
            accountId = self.redisCacheService.getValueByKey(userToken)
            if not accountId:
                return JsonResponse({"error": "유저 토큰이 유효하지 않음"}, status=status.HTTP_400_BAD_REQUEST)

            # 게시글 삭제 처리
            success = self.reviewService.requestDelete(pk, accountId)

            if success:
                return JsonResponse({"message": "블로그 포스트가 삭제되었습니다."}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "블로그 포스트 삭제 실패"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
