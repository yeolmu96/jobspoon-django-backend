#!/bin/bash

# Docker Redis 컨테이너에서 모든 토큰을 삭제하는 스크립트
# 사용법: ./delete_all_tokens.sh [패턴]

# 기본 패턴 설정 (기본값: temp_token으로 시작하는 모든 키)
PATTERN=${1:-"temp_token*"}

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
echo "삭제할 키 패턴: $PATTERN"

# 삭제 전 키 개수 확인
KEYS_BEFORE=$(docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" KEYS "$PATTERN" | wc -l)

echo "삭제 전 키 개수: $KEYS_BEFORE"

# 사용자 확인 요청
read -p "위의 패턴과 일치하는 모든 키를 삭제하시겠습니까? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
  echo "작업이 취소되었습니다."
  exit 0
fi

# 키 삭제 함수
delete_keys() {
  local pattern=$1
  
  # Docker 컨테이너 내에서 키 목록 가져오기
  docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" KEYS "$pattern" | while read key; do
    # 각 키 삭제
    docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" DEL "$key"
    echo "삭제됨: $key"
  done
}

# 키 삭제 실행
echo "키 삭제 중..."
delete_keys "$PATTERN"

# 삭제 후 키 개수 확인
KEYS_AFTER=$(docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" KEYS "$PATTERN" | wc -l)

echo "삭제 후 키 개수: $KEYS_AFTER"
echo "삭제된 키 개수: $(($KEYS_BEFORE - $KEYS_AFTER))"

# 모든 키 삭제 옵션 (위험! 주의해서 사용)
if [ "$PATTERN" == "--all" ]; then
  echo "경고: 모든 Redis 키를 삭제하려고 합니다!"
  read -p "정말로 모든 키를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다! (yes로 입력하세요): " CONFIRM_ALL
  
  if [ "$CONFIRM_ALL" == "yes" ]; then
    docker exec $REDIS_CONTAINER redis-cli -a "$REDIS_PASSWORD" FLUSHALL
    echo "모든 키가 삭제되었습니다."
  else
    echo "모든 키 삭제가 취소되었습니다."
  fi
fi
