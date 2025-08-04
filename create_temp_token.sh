#!/bin/bash

# 임시 userToken 생성 및 Redis에 저장하는 스크립트
# 사용법: ./create_temp_token.sh [account_id]

# 기본값 설정
ACCOUNT_ID=${1:-1}  # 기본값 1
TOKEN_PREFIX="temp_token"
TOKEN_VALUE="${TOKEN_PREFIX}_$(date +%s)_$RANDOM"  # 현재 시간과 랜덤 숫자를 조합하여 고유한 토큰 생성

# Docker Redis 컨테이너 이름
REDIS_CONTAINER="redis-container"

# Redis 비밀번호 설정
REDIS_PASSWORD="eddi@123"

# Docker 컨테이너가 실행 중인지 확인
if ! docker ps | grep -q $REDIS_CONTAINER; then
  echo "Error: Redis 컨테이너($REDIS_CONTAINER)가 실행 중이 아닙니다."
  exit 1
fi

echo "Redis 컨테이너: $REDIS_CONTAINER"
echo "토큰: $TOKEN_VALUE"
echo "계정 ID: $ACCOUNT_ID"

# Redis 연결 테스트
echo "Redis 연결 테스트 중..."
docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" PING

# Redis에 토큰 저장
echo "Redis에 토큰 저장 시도 중..."
REDIS_RESULT=$(docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" SET "$TOKEN_VALUE" "$ACCOUNT_ID")
echo "Redis 응답: $REDIS_RESULT"

# 결과 확인
if [ "$REDIS_RESULT" = "OK" ]; then
  echo "성공: 임시 userToken이 생성되었습니다."
  echo "userToken: $TOKEN_VALUE"
  echo "account_id: $ACCOUNT_ID"
  
  # 토큰 만료 시간 설정 (1시간)
  echo "토큰 만료 시간 설정 중..."
  docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" EXPIRE "$TOKEN_VALUE" 3600
  
  # Postman에서 사용할 수 있는 형식으로 출력
  echo ""
  echo "Postman에서 다음 JSON을 사용하세요:"
  echo "{\"userToken\": \"$TOKEN_VALUE\"}"
else
  echo "오류: Redis에 토큰을 저장하지 못했습니다."
  exit 1
fi

echo "토큰 유효 시간: 1시간"
