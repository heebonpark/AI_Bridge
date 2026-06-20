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
        
        /* Chat Bubbles */
        .chat-bubble-user {{
            background: {t['user_bubble']};
            border: 1px solid {t['glass_border']};
            border-radius: 16px 16px 0px 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            text-align: right;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .chat-bubble-ai {{
            background: {t['ai_bubble']};
            border: 1px solid {t['glass_border']};
            border-radius: 16px 16px 16px 0px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
st.title("✨ AI Bridge")
st.markdown("**Data Intel PRO** - Premium AI Agent Pipeline", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chat History Display
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        if chat['role'] == 'user':
            st.markdown(f"<div class='chat-bubble-user'>👤 <b>나:</b><br><br>{chat['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-ai'>🤖 <b>AI Bridge:</b><br><br>{chat['content']}</div>", unsafe_allow_html=True)
else:
    st.info("아직 대화 기록이 없습니다. 아래 입력창에 첫 번째 질문을 남겨주세요!")

# Input Box at the bottom
st.markdown('<div class="glass-container">', unsafe_allow_html=True)
prompt = st.text_area("어떤 도움이 필요하신가요?", height=100, placeholder="예: 오늘 서울 날씨 알려줘, 또는 이 데이터에서 이상치를 찾아줘...")

if st.button("🚀 AI 에이전트 실행"):
    if not prompt.strip():
        st.warning("질문을 입력해주세요.")
    else:
        # Save user prompt to history
        st.session_state.chat_history.append({'role': 'user', 'content': prompt})
        
        # Save prompt to input.txt
        try:
            with open("input.txt", "w", encoding="utf-8") as f:
                f.write(prompt)
        except Exception as e:
            st.error(f"입력 파일 저장 실패: {e}")
            st.stop()
            
        # Run Pipeline
        import bridge_agent
        
        with st.status("AI Bridge 실행 중...", expanded=True) as status:
            try:
                result = None
                pipeline = bridge_agent.run_pipeline()
                for step in pipeline:
                    if step.startswith("🔄") or step.startswith("🧠") or step.startswith("💾") or step.startswith("🚀"):
                        st.write(step)
                    else:
                        result = step
                
                status.update(label="실행 완료!", state="complete", expanded=False)
                
                # Save AI response to history
                st.session_state.chat_history.append({'role': 'ai', 'content': result})
                
                st.balloons()
                st.rerun() # Refresh page to show new chat bubbles cleanly
                
            except Exception as e:
                status.update(label="오류 발생", state="error", expanded=True)
                st.error(f"실행 중 오류가 발생했습니다: {e}")

st.markdown('</div>', unsafe_allow_html=True)
