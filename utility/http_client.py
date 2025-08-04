import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class HttpClient:
    _admin_client = None
    _ai_client = None

    @classmethod
    def getAdminClient(cls):
        """Fiber 서버 (Admin 용) 클라이언트"""
        if cls._admin_client is None:
            cls._admin_client = httpx.Client(
                base_url=os.getenv("FIBER_URL"),
                timeout=25
            )
        return cls._admin_client

    @classmethod
    def getAIClient(cls):
        """FastAPI 서버 (AI 용) 클라이언트"""
        if cls._ai_client is None:
            cls._ai_client = httpx.Client(
                base_url=os.getenv("FASTAPI_URL"),
                timeout=180
            )
        return cls._ai_client

    @classmethod
    def postToAdmin(cls, endpoint: str, data: dict) -> dict | bool:
        """Admin 서버로 POST 요청"""
        client = cls.getAdminClient()
        try:
            response = client.post(endpoint, json=data, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Admin 서버 응답 오류: {response.status_code}")
                return False
        except httpx.RequestError as exc:
            print(f"⚠️ Admin 서버 요청 에러: {str(exc)}")
            return False

    @classmethod
    def postToAI(cls, endpoint: str, data: dict) -> dict | bool:
        """AI 서버로 POST 요청"""
        client = cls.getAIClient()
        try:
            response = client.post(endpoint, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ AI 서버 응답 오류: {response.status_code}")
                return False
        except httpx.RequestError as exc:
            print(f"⚠️ AI 서버 요청 에러: {str(exc)}")
            return False

    @classmethod
    def close(cls):
        """모든 클라이언트 종료"""
        if cls._admin_client:
            cls._admin_client.close()
            cls._admin_client = None
        if cls._ai_client:
            cls._ai_client.close()
            cls._ai_client = None

    @classmethod
    def getFromAI(cls, endpoint: str) -> dict | bool:
        """AI 서버로 GET 요청"""
        client = cls.getAIClient()
        try:
            response = client.get(endpoint)
            if response.status_code in (200, 202, 404):  # 상황별 상태 확인
                return response.json()
            else:
                print(f"❌ AI 서버 GET 응답 오류: {response.status_code}")
                return False
        except httpx.RequestError as exc:
            print(f"⚠️ AI 서버 GET 요청 에러: {str(exc)}")
            return False
