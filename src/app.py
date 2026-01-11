# app.py
import streamlit as st
import time
from logic.guardian_brain import GuardianBrain

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cognitive Guardian",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Graceful fail

local_css("assets/chatgpt.css")

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None # Triggers Pop-up
if "guardian" not in st.session_state:
    st.session_state.guardian = GuardianBrain()

# --- SIDEBAR (ChatGPT Style) ---
with st.sidebar:
    # "New Chat" Button
    if st.button("➕ New chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("History")
    st.markdown("Math Homework Help", help="Demo History Item")
    st.markdown("Python Logic", help="Demo History Item")
    
    st.markdown("---")
    
    # Profile Display at Bottom
    if st.session_state.user_profile:
        p = st.session_state.user_profile
        st.markdown(f"""
            <div style="background: #343541; padding: 10px; border-radius: 6px; display: flex; align-items: center; gap: 10px;">
                <div style="background: #10a37f; color: white; width: 30px; height: 30px; border-radius: 4px; display: flex; justify-content: center; align-items: center; font-weight: bold;">
                    {p['name'][0].upper()}
                </div>
                <div style="line-height: 1.2;">
                    <div style="color: white; font-weight: 500; font-size: 0.9em;">{p['name']}</div>
                    <div style="color: #bbb; font-size: 0.75em;">{p['role']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Log out / Reset"):
            st.session_state.user_profile = None
            st.session_state.messages = []
            st.rerun()

# --- 🚀 POP-UP ONBOARDING (DEMO MODE) ---
if st.session_state.user_profile is None:
    # 3-Column Layout to Center the Form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## Welcome to Cognitive Guardian")
        st.markdown("Please verify your identity to begin.")
        
        with st.form("onboarding"):
            name = st.text_input("Name", placeholder="e.g. Alex")
            role = st.selectbox("Role", ["Student", "Child (Explorer)", "Developer", "Professional"])
            style = st.selectbox("Thinking Style", ["Visual", "Logical", "Direct"])
            
            if st.form_submit_button("Enter Guardian OS"):
                if name:
                    st.session_state.user_profile = {
                        "name": name,
                        "role": role,
                        "style": style,
                        "age": 10 if "Child" in role else 25
                    }
                    st.rerun()
    st.stop() # Halts app here until login

# --- 💬 MAIN CHAT INTERFACE ---

# 1. Empty State Greeting
if not st.session_state.messages:
    st.markdown("""
        <div style="text-align: center; margin-top: 15vh;">
            <div style="background: #444654; display: inline-block; padding: 15px; border-radius: 50%; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 30px;">🧠</h1>
            </div>
            <h1 style="color: white;">Cognitive Guardian</h1>
        </div>
    """, unsafe_allow_html=True)

# 2. Chat History
for msg in st.session_state.messages:
    # Dynamic Avatars
    avatar = "🦖" if msg["role"] == "user" else "🧠"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 3. Input & Logic
if prompt := st.chat_input("Message Cognitive Guardian..."):
    
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🦖"):
        st.markdown(prompt)

    # Show AI Response
    with st.chat_message("assistant", avatar="🧠"):
        msg_placeholder = st.empty()
        full_response = ""
        
        # Thinking Spinner
        with st.spinner("Thinking..."):
            prof = st.session_state.user_profile
            response_text = st.session_state.guardian.generate_response(
                prompt, st.session_state.messages, 
                prof['age'], prof['role'], prof['style']
            )
        
        # Typing Animation
        for char in response_text.split(" "):
            full_response += char + " "
            msg_placeholder.markdown(full_response + "▌")
            time.sleep(0.04)
        
        msg_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
