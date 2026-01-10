import sys
import os

# Add the project root to the system path so Python can find 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import time
from src.logic.guardian import CognitiveGuardian
from src.logic.profiles import UserProfile

# --- Page Config ---
st.set_page_config(
    page_title="Cognitive Guardian Layer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("src/assets/style.css")
except FileNotFoundError:
    st.warning("Style file not found. Running with default styles.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "guardian" not in st.session_state:
    try:
        st.session_state.guardian = CognitiveGuardian()
    except Exception as e:
        st.error(f"Failed to initialize AI: {e}")
        st.stop()

# --- Sidebar: User Profile Engine ---
with st.sidebar:
    st.title("👤 Identity Layer")
    st.markdown("---")
    
    age = st.slider("User Age", 5, 80, 12)
    role = st.selectbox("Occupation/Role", ["Student", "Engineer", "Doctor", "Artist", "Curious Learner"])
    style = st.select_slider("Learning Style", options=["Visual", "Verbal", "Logical", "Kinesthetic"])
    
    st.markdown("---")
    st.markdown("### 🛡️ Guardian Status")
    st.success("System: ONLINE")
    st.info(f"Mode: {('Socratic' if age > 10 else 'Playful')}")
    
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- Main Interface ---
st.markdown("""
    <h1 style='text-align: center; color: white;'>
    Cognitive <span style='color: #FF4B4B;'>Guardian</span>
    </h1>
    <p style='text-align: center; opacity: 0.7;'>
    The AI that makes you think before it answers.
    </p>
""", unsafe_allow_html=True)

# Build Profile Object
current_profile = UserProfile(age=age, role=role, cognitive_style=style, competence="Beginner")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Logic ---
if prompt := st.chat_input("Ask me anything..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Guardian Reasoning (Visual Feedback)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Simulate "Thinking" analysis phase
        with st.status("Analysing cognitive load...", expanded=True) as status:
            st.write("Checking safety protocols...")
            time.sleep(0.5)
            st.write(f"Adapting to age {age} profile...")
            time.sleep(0.5)
            st.write("Constructing Socratic scaffold...")
            time.sleep(0.5)
            status.update(label="Guardian ready", state="complete", expanded=False)
        
        # 3. Stream Response
        full_response = ""
        try:
            # Call the Guardian Middleware
            stream = st.session_state.guardian.process_interaction(
                prompt, 
                current_profile, 
                st.session_state.messages
            )
            
            for chunk in stream:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01) # Typing effect
                
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
            full_response = "I'm having trouble connecting to my neural core. Please check your API keys."

    # 4. Save Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": full_response})