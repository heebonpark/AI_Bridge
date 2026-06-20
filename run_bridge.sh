#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

echo "📦 필요한 라이브러리 확인 및 설치 중..."
python3 -m pip install -r requirements.txt -q

# .env 파일이 없으면 .env.example 복사 (처음 실행 시)
if [ ! -f .env ]; then
    echo "⚠️ .env 파일이 없습니다. .env.example을 복사하여 생성합니다."
    cp .env.example .env
    echo "💡 주의: .env 파일을 열고 GEMINI_API_KEY를 본인의 키로 꼭 수정해주세요!"
    exit 1
fi

echo "🚀 AI Bridge Agent (GUI Version) 시작..."
streamlit run app.py
