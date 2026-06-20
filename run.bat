@echo off
cd C:\Users\사용자명\AI_Bridge
:: 1. GitHub에서 새로운 질문 가져오기
git pull origin main

:: 2. 파이썬 AI 에이전트 실행 (Gemini API 호출)
python agent_process.py

:: 3. 결과물 저장 후 GitHub으로 자동 업로드
git add .
git commit -m "AI processed at %date% %time%"
git push origin main
pause