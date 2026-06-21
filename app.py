import streamlit as st
import os
import sys

# Configure page
st.set_page_config(
    page_title="AI Bridge - Data Intel PRO",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme definitions
THEMES = {
    "Dark Navy (기본)": {
        "bg_color": "#0f172a",
        "text_color": "#f8fafc",
        "glass_bg": "rgba(30, 41, 59, 0.7)",
        "glass_border": "rgba(255, 255, 255, 0.1)",
        "btn_gradient": "linear-gradient(135deg, #2563eb, #1d4ed8)",
        "btn_hover": "rgba(37, 99, 235, 0.4)",
        "input_bg": "rgba(15, 23, 42, 0.8)",
        "input_border": "#334155",
        "input_focus": "#2563eb",
        "user_bubble": "rgba(37, 99, 235, 0.2)",
        "ai_bubble": "rgba(51, 65, 85, 0.4)"
    },
    "Midnight Purple": {
        "bg_color": "#1a1025",
        "text_color": "#f3e8ff",
        "glass_bg": "rgba(43, 20, 61, 0.7)",
        "glass_border": "rgba(255, 255, 255, 0.1)",
        "btn_gradient": "linear-gradient(135deg, #a855f7, #7e22ce)",
        "btn_hover": "rgba(168, 85, 247, 0.4)",
        "input_bg": "rgba(26, 16, 37, 0.8)",
        "input_border": "#581c87",
        "input_focus": "#a855f7",
        "user_bubble": "rgba(168, 85, 247, 0.2)",
        "ai_bubble": "rgba(67, 30, 94, 0.4)"
    },
    "Emerald Ocean": {
        "bg_color": "#064e3b",
        "text_color": "#ecfdf5",
        "glass_bg": "rgba(6, 95, 70, 0.7)",
        "glass_border": "rgba(255, 255, 255, 0.1)",
        "btn_gradient": "linear-gradient(135deg, #10b981, #059669)",
        "btn_hover": "rgba(16, 185, 129, 0.4)",
        "input_bg": "rgba(6, 78, 59, 0.8)",
        "input_border": "#047857",
        "input_focus": "#10b981",
        "user_bubble": "rgba(16, 185, 129, 0.2)",
        "ai_bubble": "rgba(6, 95, 70, 0.4)"
    },
    "Sunset Ruby": {
        "bg_color": "#4c0519",
        "text_color": "#fff1f2",
        "glass_bg": "rgba(136, 19, 55, 0.7)",
        "glass_border": "rgba(255, 255, 255, 0.1)",
        "btn_gradient": "linear-gradient(135deg, #f43f5e, #e11d48)",
        "btn_hover": "rgba(244, 63, 94, 0.4)",
        "input_bg": "rgba(76, 5, 25, 0.8)",
        "input_border": "#9f1239",
        "input_focus": "#f43f5e",
        "user_bubble": "rgba(244, 63, 94, 0.2)",
        "ai_bubble": "rgba(136, 19, 55, 0.4)"
    },
    "Silver Frost (Light Mode)": {
        "bg_color": "#f1f5f9",
        "text_color": "#0f172a",
        "glass_bg": "rgba(255, 255, 255, 0.8)",
        "glass_border": "rgba(0, 0, 0, 0.1)",
        "btn_gradient": "linear-gradient(135deg, #334155, #0f172a)",
        "btn_hover": "rgba(51, 65, 85, 0.4)",
        "input_bg": "rgba(248, 250, 252, 0.8)",
        "input_border": "#cbd5e1",
        "input_focus": "#334155",
        "user_bubble": "rgba(51, 65, 85, 0.1)",
        "ai_bubble": "rgba(255, 255, 255, 0.9)"
    }
}

# Sidebar - Theme Selection
st.sidebar.title("🎨 테마 설정")
selected_theme_name = st.sidebar.selectbox("프리미엄 테마 선택", list(THEMES.keys()))
theme = THEMES[selected_theme_name]

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ AI Bridge 정보")
st.sidebar.info("- **모델:** gemini-2.5-flash\n- **역할:** Data Intel PRO\n- **동기화:** GitHub 자동 연동")

# Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.sidebar.markdown("---")
st.sidebar.markdown("### 💾 데이터 내보내기")
if st.session_state.chat_history:
    chat_text = ""
    for chat in st.session_state.chat_history:
        role = "나" if chat['role'] == 'user' else "AI Bridge"
        chat_text += f"[{role}]\n{chat['content']}\n\n"
    st.sidebar.download_button(
        label="📥 전체 대화 내용 다운로드 (TXT)",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
        use_container_width=True
    )
else:
    st.sidebar.info("대화 내역이 없습니다.")

def get_custom_css(t):
    return f"""
    <style>
        /* Import Pretendard font */
        @import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");
        
        html, body, [class*="css"] {{
            font-family: 'Pretendard', sans-serif !important;
        }}
        
        /* Background and theme colors */
        .stApp {{
            background-color: {t['bg_color']};
            color: {t['text_color']};
        }}
        
        /* Hide Streamlit default UI */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Glassmorphism Container */
        .glass-container {{
            background: {t['glass_bg']};
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid {t['glass_border']};
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            color: {t['text_color']};
        }}
        
        /* Chat Layout */
        .chat-row-user {{
            display: flex;
            justify-content: flex-end;
            margin-bottom: 1rem;
        }}
        .chat-row-ai {{
            display: flex;
            justify-content: flex-start;
            margin-bottom: 2rem;
        }}
        .chat-bubble-user {{
            background: {t['user_bubble']};
            border: 1px solid {t['glass_border']};
            border-radius: 20px 20px 4px 20px;
            padding: 1.2rem 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            max-width: 80%;
            color: {t['text_color']};
            line-height: 1.6;
        }}
        .chat-bubble-ai {{
            background: {t['ai_bubble']};
            border: 1px solid {t['glass_border']};
            border-radius: 20px 20px 20px 4px;
            padding: 1.2rem 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            max-width: 80%;
            color: {t['text_color']};
            line-height: 1.6;
        }}
        
        /* Buttons */
        .stButton>button {{
            background: {t['btn_gradient']};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px {t['btn_hover']};
            color: white;
            border: none;
        }}
        
        /* Text Area */
        .stTextArea textarea {{
            background-color: {t['input_bg']} !important;
            color: {t['text_color']} !important;
            border: 1px solid {t['input_border']} !important;
            border-radius: 12px !important;
        }}
        .stTextArea textarea:focus {{
            border-color: {t['input_focus']} !important;
            box-shadow: 0 0 0 2px {t['btn_hover']} !important;
        }}
        
        /* Mobile Optimization */
        @media (max-width: 768px) {{
            .glass-container {{
                padding: 1rem;
                margin-bottom: 1rem;
                border-radius: 12px;
            }}
            .chat-bubble-user, .chat-bubble-ai {{
                padding: 1rem;
                font-size: 0.95rem;
            }}
            .stButton>button {{
                padding: 0.6rem 1rem;
            }}
            h1 {{
                font-size: 1.8rem !important;
            }}
        }}
    </style>
    """

# Apply dynamic CSS
st.markdown(get_custom_css(theme), unsafe_allow_html=True)

# Header
st.markdown(f'''
<div class="glass-container" style="text-align: center; padding: 2rem 1rem; margin-top: 1rem;">
    <h1 style="margin-bottom: 0.5rem; font-size: 2.8rem; font-weight: 800; background: {theme['btn_gradient']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">✨ AI Bridge</h1>
    <p style="margin-top: 0; font-size: 1.1rem; opacity: 0.8;"><b>Data Intel PRO</b> - Premium AI Agent Pipeline</p>
</div>
''', unsafe_allow_html=True)

# Chat History Display
if st.session_state.chat_history:
    for i, chat in enumerate(st.session_state.chat_history):
        if chat['role'] == 'user':
            st.markdown(f"<div class='chat-row-user'><div class='chat-bubble-user'>👤 <b>나:</b><br><br>{chat['content']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-row-ai'><div class='chat-bubble-ai'>🤖 <b>AI Bridge:</b><br><br>{chat['content']}</div></div>", unsafe_allow_html=True)
            # Add download button for the latest AI response
            if i == len(st.session_state.chat_history) - 1:
                col1, col2 = st.columns([8, 2])
                with col2:
                    st.download_button(
                        label="📥 이 답변만 다운로드",
                        data=chat['content'],
                        file_name="ai_response.txt",
                        mime="text/plain",
                        key=f"download_{i}",
                        use_container_width=True
                    )
else:
    st.info("아직 대화 기록이 없습니다. 아래 입력창에 첫 번째 질문을 남겨주세요!")

# Input Box at the bottom (Removed broken HTML wrapper)
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    uploaded_file = st.file_uploader("📎 파일 또는 이미지 첨부", type=["png", "jpg", "jpeg", "pdf", "csv", "txt", "xlsx"])
with col2:
    prompt = st.text_area("어떤 도움이 필요하신가요?", height=68, placeholder="예: 첨부된 영수증 분석, 내일 날씨 확인...")

if st.button("🚀 AI 에이전트 실행"):
    if not prompt.strip() and not uploaded_file:
        st.warning("질문을 입력하거나 파일을 첨부해주세요.")
    else:
        # Save user prompt to history
        user_msg = prompt
        if uploaded_file:
            user_msg = f"*(첨부파일: {uploaded_file.name})*\n\n" + user_msg
        st.session_state.chat_history.append({'role': 'user', 'content': user_msg})
        
        # Handle file upload to temporary local directory
        temp_file_path = None
        is_data_file = False
        ml_results = None
        if uploaded_file:
            import uuid
            temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Use safe ASCII filename to prevent UnicodeEncodeError in google-genai SDK
            _, ext = os.path.splitext(uploaded_file.name)
            ext_lower = ext.lower()
            safe_filename = f"upload_{uuid.uuid4().hex}{ext_lower}"
            temp_file_path = os.path.join(temp_dir, safe_filename)
            
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            if ext_lower in ['.csv', '.xlsx']:
                is_data_file = True
                try:
                    from ml_analyzer import MLAnalyzer
                    st.info("📊 데이터 분석 대시보드를 준비 중입니다...")
                    analyzer = MLAnalyzer(temp_file_path)
                    st.dataframe(analyzer.df.head(5), use_container_width=True)
                    
                    # Run Anomaly Detection
                    ml_results = analyzer.run_anomaly_detection()
                    if ml_results and ml_results.get("fig"):
                        st.plotly_chart(ml_results["fig"], use_container_width=True)
                        # Append ML insights to prompt
                        prompt += f"\n\n[자동 머신러닝 분석 결과]\n{ml_results['report']}\n다음 통계 요약을 바탕으로 이 데이터의 비즈니스 인사이트와 해결책을 제시해줘:\n{analyzer.get_summary_stats()}"
                except Exception as e:
                    st.warning(f"ML 자동 분석 중 에러가 발생했습니다: {e}")
        
        # Run Pipeline
        import bridge_agent
        import importlib
        importlib.reload(bridge_agent)
        
        with st.status("AI Bridge 실행 중...", expanded=True) as status:
            try:
                result = None
                pipeline = bridge_agent.run_pipeline(prompt_text=prompt, file_path=temp_file_path)
                for step in pipeline:
                    if step.startswith("🔄") or step.startswith("🧠") or step.startswith("💾") or step.startswith("🚀"):
                        st.write(step)
                    else:
                        result = step
                
                status.update(label="실행 완료!", state="complete", expanded=False)
                
                # Cleanup temp file
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                
                # Save AI response to history
                st.session_state.chat_history.append({'role': 'ai', 'content': result})
                
                st.balloons()
                st.rerun() # Refresh page to show new chat bubbles cleanly
                
            except Exception as e:
                status.update(label="오류 발생", state="error", expanded=True)
                st.error(f"실행 중 오류가 발생했습니다: {e}")
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
