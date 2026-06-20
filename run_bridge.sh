#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# API 키 설정 확인
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY 환경변수가 설정되어 있지 않습니다."
    echo "💡 사용법: 터미널에서 아래 명령어를 먼저 입력하세요."
    echo "export GEMINI_API_KEY=\"여기에_본인의_API_키를_입력하세요\""
    echo "그 다음 ./run_bridge.sh 를 실행하세요."
    exit 1
fi

echo "🚀 AI Bridge Agent 시작..."
python3 bridge_agent.py
