import os
import subprocess
import google.generativeai as genai

# 현재 스크립트가 위치한 디렉토리를 REPO_PATH로 자동 설정
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.getenv("GEMINI_API_KEY")

def run_command(command):
    """쉘 명령어를 실행하고 결과를 반환하는 헬퍼 함수"""
    print(f"[실행] {command}")
    result = subprocess.run(command, cwd=REPO_PATH, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ 명령어 실행 오류 ({command}):")
        print(result.stderr.strip())
    else:
        if result.stdout.strip():
            print(result.stdout.strip())
    return result

def main():
    if not API_KEY:
        print("❌ Error: 'GEMINI_API_KEY' 환경 변수가 설정되어 있지 않습니다.")
        print("실행 전에 'export GEMINI_API_KEY=당신의키' 명령어를 입력해주세요.")
        return

    # Gemini 모델 초기화
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro') # 필요시 gemini-1.5-pro-latest 등으로 변경 가능

    print("--- 🔄 Git 동기화 시작 ---")
    run_command("git pull origin main")

    # 질문 읽기
    input_file = os.path.join(REPO_PATH, "input.txt")
    if not os.path.exists(input_file):
        print(f"❌ Error: 입력 파일이 없습니다 ({input_file})")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        prompt = f.read().strip()
    
    if not prompt:
        print("⚠️ 질문(input.txt)이 비어있습니다. 종료합니다.")
        return

    # AI 처리
    print(f"\n--- 🧠 AI 처리 중 ---")
    print(f"질문 내용: {prompt[:50]}{'...' if len(prompt) > 50 else ''}")
    
    try:
        response = model.generate_content(prompt)
        output_text = response.text
    except Exception as e:
        print(f"❌ AI 처리 중 예외 발생: {e}")
        return
    
    # 결과 저장
    output_file = os.path.join(REPO_PATH, "output.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)
    print(f"✅ 결과 저장 완료: output.txt (길이: {len(output_text)} 자)")
    
    # 자동 푸시
    print("\n--- 🚀 GitHub 업로드 중 ---")
    run_command("git add output.txt")
    
    # 변경사항이 있는지 확인 후 커밋
    status = run_command("git status --porcelain")
    if "output.txt" in status.stdout:
        run_command('git commit -m "🤖 AI processed answer [skip ci]"')
        run_command("git push origin main")
        print("🎉 완료: 결과가 GitHub에 성공적으로 업로드되었습니다.")
    else:
        print("ℹ️ 변경사항이 없어 커밋하지 않았습니다.")

if __name__ == "__main__":
    main()