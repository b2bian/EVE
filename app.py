"""
EVE - AI Companion with Gemini Intelligence
Beautiful, responsive web UI with real-time chat, voice I/O, and advanced memory system
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.personal_brain import PersonalBrain
from utils.memory import MemoryManager
from utils.ollama_handler import OllamaHandler
from utils.system_prompts import get_system_prompt, PERSONALITY_DESCRIPTIONS

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="EVE | AI Companion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# THEME & STYLING
# ============================================================================

st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%);
        color: #e0e0e0;
    }
    
    .main {
        background: #0a0e27;
        padding: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #00d4ff;
    }
    
    /* Custom Cards */
    .card {
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border: 1px solid #00d4ff;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
        animation: slideIn 0.5s ease-out;
    }
    
    .card:hover {
        border-color: #ff006e;
        box-shadow: 0 12px 48px rgba(255, 0, 110, 0.15);
    }
    
    /* Status Indicators */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    
    .status-online {
        background: linear-gradient(135deg, #00d4ff 0%, #00a8cc 100%);
        color: #0a0e27;
    }
    
    .status-offline {
        background: linear-gradient(135deg, #666 0%, #444 100%);
        color: #e0e0e0;
    }
    
    .status-thinking {
        background: linear-gradient(135deg, #ffa502 0%, #ff7c00 100%);
        color: #0a0e27;
        animation: pulse 1s infinite;
    }
    
    /* Chat Container */
    .chat-container {
        background: #0f3460;
        border-radius: 12px;
        padding: 1.5rem;
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #00d4ff;
    }
    
    .message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 8px;
        animation: fadeIn 0.3s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #00d4ff 0%, #00a8cc 100%);
        margin-left: 2rem;
        color: #0a0e27;
        font-weight: 500;
    }
    
    .eve-message {
        background: linear-gradient(135deg, #ff006e 0%, #cc0066 100%);
        margin-right: 2rem;
        color: #fff;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #00a8cc 100%);
        color: #0a0e27;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00a8cc 0%, #0088aa 100%);
        box-shadow: 0 6px 25px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00d4ff;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Input styling */
    .stTextInput input, .stTextArea textarea {
        background: #0f3460 !important;
        color: #e0e0e0 !important;
        border: 1px solid #00d4ff !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox, .stslider {
        color: #e0e0e0;
    }
    
    /* Tabs */
    [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid #00d4ff;
    }
    
    [aria-selected="true"] {
        color: #00d4ff !important;
        border-bottom: 3px solid #00d4ff !important;
    }
    
    [aria-selected="false"] {
        color: #999 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.brain = PersonalBrain()
    st.session_state.memory = MemoryManager("memory/memory.json")
    st.session_state.ollama = OllamaHandler({})
    
    # Try to load Gemini
    try:
        from utils.gemini_handler import GeminiHandler
        st.session_state.gemini = GeminiHandler({})
    except Exception as e:
        st.session_state.gemini = None
        print(f"Gemini not available: {e}")
    
    # Try to load voice
    try:
        from utils.voice import VoiceHandler
        st.session_state.voice_handler = VoiceHandler({})
    except Exception as e:
        st.session_state.voice_handler = None
        print(f"Voice not available: {e}")
    
    st.session_state.chat_messages = []
    st.session_state.current_personality = "quirky"
    st.session_state.voice_enabled = True
    st.session_state.voice_listening = False
    st.session_state.selected_voice_id = None
    st.session_state.voice_rate = 150
    st.session_state.voice_volume = 0.9
    st.session_state.last_handled_transcript = ""

# ============================================================================
# MAIN LAYOUT
# ============================================================================

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <h1 style="text-align: center; margin-bottom: 0.5rem;">✨ EVE</h1>
    <p style="text-align: center; color: #00d4ff; font-size: 0.9rem; margin: 0;">
        Your Personal AI Companion
    </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main content with sidebar
with st.sidebar:
    st.markdown("### ⚙️ CONTROL PANEL")
    st.markdown("---")
    
    # System Status
    st.markdown("#### 📡 System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        gemini_ok = st.session_state.gemini and st.session_state.gemini.check_connection()
        status_text = "✅ Ready" if gemini_ok else "⏳ Offline"
        st.markdown(f'<div class="status-badge status-online">{status_text}</div>', unsafe_allow_html=True)
        st.caption("Gemini API")
    
    with col2:
        ollama_ok = st.session_state.ollama.check_connection()
        status_text = "✅ Ready" if ollama_ok else "❌ Offline"
        status_class = "status-online" if ollama_ok else "status-offline"
        st.markdown(f'<div class="status-badge {status_class}">{status_text}</div>', unsafe_allow_html=True)
        st.caption("Ollama AI")
    
    if not gemini_ok and not ollama_ok:
        st.error("⚠️ No AI service available. Start Ollama or enable Gemini API.")
    
    st.markdown("---")
    
    # Personality Selection
    st.markdown("#### 🎭 Personality")
    personality = st.selectbox(
        "Choose EVE's personality:",
        list(PERSONALITY_DESCRIPTIONS.keys()),
        index=list(PERSONALITY_DESCRIPTIONS.keys()).index(st.session_state.current_personality),
        key="personality_select"
    )
    st.session_state.current_personality = personality
    st.caption(PERSONALITY_DESCRIPTIONS[personality][:100] + "...")
    
    st.markdown("---")
    
    # Voice Settings
    if st.session_state.voice_handler:
        st.markdown("#### 🎤 Voice Settings")

        voice_enabled = st.checkbox("Enable Voice (TTS)", value=st.session_state.voice_enabled)
        st.session_state.voice_enabled = voice_enabled

        st.markdown("**Voice recorder**")
        is_listening = st.session_state.voice_listening
        if st.button("▶️ Start Recording", use_container_width=True):
            st.session_state.voice_handler.start_listening()
            st.session_state.voice_listening = True
            st.success("Voice recording started. Speak now...")

        if st.button("⏹ Stop Recording", use_container_width=True):
            st.session_state.voice_handler.stop_listening()
            st.session_state.voice_listening = False
            st.success("Voice recording stopped.")

        latest_transcript = st.session_state.voice_handler.get_last_transcript()
        if latest_transcript:
            st.info(f"Latest transcript: {latest_transcript}")
            if st.button("📥 Insert transcript into input"):
                st.session_state.user_input = latest_transcript

        if voice_enabled:
            try:
                voices = st.session_state.voice_handler.get_available_voices()
                female_voices = [v for v in voices if v['is_female']]
                
                if not voices:
                    st.warning("No TTS voices available. Install platform TTS voices or check pyttsx3 setup.")
                else:
                    voice_options = female_voices if female_voices else voices
                    voice_names = [v['name'] for v in voice_options]
                    voice_ids = [v['id'] for v in voice_options]

                    selected = st.selectbox(
                        "Select voice:",
                        voice_names,
                        index=voice_names.index(st.session_state.selected_voice_id) if st.session_state.selected_voice_id in voice_names else 0,
                        key="selected_tts_voice"
                    )
                    selected_index = voice_names.index(selected)
                    st.session_state.selected_voice_id = voice_ids[selected_index]
                    st.session_state.voice_handler.set_voice(st.session_state.selected_voice_id)

                # Voice controls
                col1, col2 = st.columns(2)
                with col1:
                    speed = st.slider("Speed", 50, 300, st.session_state.voice_rate, 10)
                    st.session_state.voice_rate = speed
                    st.session_state.voice_handler.set_voice_rate(speed)

                with col2:
                    volume = st.slider("Volume", 0.0, 1.0, st.session_state.voice_volume, 0.05)
                    st.session_state.voice_volume = volume
                    st.session_state.voice_handler.set_voice_volume(volume)

                if st.button("🔊 Test Voice", use_container_width=True):
                    with st.spinner("Playing..."):
                        if not st.session_state.voice_handler.speak("Hello! I'm EVE, your AI companion."):
                            st.error("TTS failed. Check pyttsx3 and system audio output.")
                        else:
                            st.success("Voice test complete!")
            except Exception as e:
                st.warning(f"Voice setup issue: {e}")
    
    st.markdown("---")
    
    # Profile Info
    st.markdown("#### 👤 Your Profile")
    profile = st.session_state.brain.user_data
    if profile:
        st.metric("Name", profile.get("user_name", "Unknown"))
        sessions = len(profile.get("learning_history", []))
        st.metric("Sessions", sessions)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("#### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
    
    with col2:
        if st.button("💾 Save Profile", use_container_width=True):
            st.session_state.brain.log_session()
            st.success("Saved!")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

# Chat Interface
st.markdown("### 💬 Chat with EVE")

# Display chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="message user-message">👤 You: {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message eve-message">✨ EVE: {msg["content"]}</div>', unsafe_allow_html=True)

# Apply any new voice transcript to input
if st.session_state.voice_handler:
    latest = st.session_state.voice_handler.get_last_transcript()
    if latest and latest != st.session_state.last_handled_transcript:
        st.session_state.last_handled_transcript = latest
        st.session_state.user_input = latest
        st.info("🎙 Voice transcript auto-filled. Press Send to submit.")

# Input interface
st.markdown("---")
st.markdown("#### 📝 Send a Message")

col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Type your message:",
        placeholder="Tell EVE something...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", use_container_width=True, type="primary")

# Voice input option
col1, col2 = st.columns([4, 1])
with col1:
    st.caption("Or use voice input below")
with col2:
    if st.session_state.voice_handler:
        st.caption("🎤 Available")

# Handle message submission
if send_button and user_input:
    # Add user message to history
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Show thinking
    with st.container():
        st.markdown('<div class="status-badge status-thinking">🧠 EVE is thinking...</div>', unsafe_allow_html=True)
        
        try:
            # Get system prompt
            system_prompt = st.session_state.brain.get_system_prompt_for_personality(
                st.session_state.current_personality
            )
            
            # Build context from recent messages
            context = ""
            if st.session_state.chat_messages:
                recent = st.session_state.chat_messages[-10:]
                for msg in recent:
                    role = "You" if msg["role"] == "user" else "EVE"
                    context += f"{role}: {msg['content']}\n"
            
            full_prompt = f"{system_prompt}\n\nRecent chat:\n{context}\nUser: {user_input}\n\nEVE:"
            
            # Use Gemini first when available, otherwise fallback to Ollama.
            response = None
            gemini_available = st.session_state.gemini and st.session_state.gemini.check_connection()
            ollama_available = st.session_state.ollama and st.session_state.ollama.check_connection()

            if gemini_available:
                response = st.session_state.gemini.generate(full_prompt, stream=False)
                # If Gemini fails (disabled/forbidden), disable and fallback.
                if isinstance(response, str) and "Gemini API error" in response:
                    st.warning("⚠️ Gemini API error detected. Falling back to Ollama if available.")
                    if ollama_available:
                        response = st.session_state.ollama.generate(full_prompt, stream=False)
                    else:
                        response = response

            if response is None or (isinstance(response, str) and response.strip() == ""):
                if ollama_available:
                    response = st.session_state.ollama.generate(full_prompt, stream=False)
                else:
                    response = "Error: No AI backend available. Please start Ollama or enable Gemini API."

            # Clean response
            response = response.strip() if isinstance(response, str) else str(response)
            if response.startswith("EVE:"):
                response = response[4:].strip()
            
            # Add to history
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Save to memory
            st.session_state.memory.add_conversation("user", user_input)
            st.session_state.memory.add_conversation("assistant", response)
            
            # Voice output
            if st.session_state.voice_enabled and st.session_state.voice_handler:
                st.session_state.voice_handler.speak_async(response)
            
            st.success("✅ Response received!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            print(f"Full error: {e}")
            import traceback
            traceback.print_exc()

# Bottom info
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #666; font-size: 0.85rem;">
    EVE v2.0 | Powered by Gemini + Ollama | 🔐 Your data stays local
</p>
""", unsafe_allow_html=True)
