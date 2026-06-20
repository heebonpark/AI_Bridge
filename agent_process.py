import os
import google.generativeai as genai

# 환경 변수로 API Key 안전하게 관리
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

def process_tasks():
    with open("input.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    
    # Gemini API 호출
    response = model.generate_content(prompt)
    
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    process_tasks()