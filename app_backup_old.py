"""
EVE - Cyberpunk AI Desktop Assistant
Web UI powered by Streamlit with Dynamic Visuals & Voice Integration
"""
import streamlit as st
import sys
import os
import json
import time
from pathlib import Path

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.personal_brain import PersonalBrain
from utils.memory import MemoryManager
from utils.ollama_handler import OllamaHandler
from utils.system_prompts import get_system_prompt, PERSONALITY_DESCRIPTIONS
from utils.theme_loader import ThemeLoader

# Page config
st.set_page_config(
    page_title="EVE - AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cyberpunk theme with animations
st.markdown("""
<style>
:root {
    --bg: #0d0d0d;
    --secondary-bg: #1a1a1a;
    --accent-cyan: #00f2ff;
    --accent-orange: #ff9d00;
    --text-primary: #e0e0e0;
}

@keyframes glow {
    0%, 100% { text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff; }
    50% { text-shadow: 0 0 20px #00f2ff, 0 0 30px #ff9d00, 0 0 40px #00f2ff; }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(0, 242, 255, 0.7); }
    50% { box-shadow: 0 0 0 10px rgba(0, 242, 255, 0); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes scan {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Main bg */
.main {
    background-color: #0d0d0d;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1a1a1a;
    border-right: 2px solid #00f2ff;
}

/* Profile Images */
.profile-image {
    border-radius: 50%;
    border: 3px solid #00f2ff;
    box-shadow: 0 0 20px #00f2ff;
    animation: pulse 2s infinite;
    width: 120px;
    height: 120px;
    object-fit: cover;
}

/* EVE Avatar with glow */
.eve-avatar {
    border-radius: 50%;
    border: 3px solid #ff9d00;
    box-shadow: 0 0 30px #ff9d00;
    animation: pulse 1.5s infinite;
    width: 100px;
    height: 100px;
    object-fit: cover;
}

/* Headers with glow */
h1, h2, h3 {
    color: #00f2ff;
    animation: glow 3s ease-in-out infinite;
}

/* Chat messages */
.stChatMessage {
    background-color: #1a1a1a;
    border: 1px solid #00f2ff;
    border-radius: 8px;
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00f2ff, #ff9d00);
    color: #0d0d0d;
    border: 2px solid #00f2ff;
    font-weight: bold;
    animation: pulse 2s infinite;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ff9d00, #00f2ff);
    transform: scale(1.05);
    box-shadow: 0 0 20px #ff9d00;
}

/* Input boxes */
.stTextInput > div > div > input,
.stSelectbox > div > div > select {
    background-color: #1a1a1a;
    color: #00f2ff;
    border: 2px solid #00f2ff;
    border-radius: 5px;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus {
    box-shadow: 0 0 20px #00f2ff;
    border-color: #ff9d00;
}

/* Metrics */
.stMetric {
    background-color: #1a1a1a;
    padding: 15px;
    border-radius: 8px;
    border: 2px solid #00f2ff;
    box-shadow: 0 0 10px rgba(0, 242, 255, 0.3);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] button {
    color: #e0e0e0;
    border-bottom: 2px solid transparent;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #00f2ff;
    border-bottom: 3px solid #ff9d00;
    box-shadow: 0 0 10px #00f2ff;
}

.stTabs [data-baseweb="tab-list"] button:hover {
    color: #ff9d00;
}

/* Status indicator */
.status-online {
    display: inline-block;
    width: 12px;
    height: 12px;
    background-color: #00f2ff;
    border-radius: 50%;
    animation: pulse 1s infinite;
    margin-right: 8px;
}

.status-offline {
    display: inline-block;
    width: 12px;
    height: 12px;
    background-color: #ff4444;
    border-radius: 50%;
    margin-right: 8px;
}

/* Expandable sections */
.streamlit-expanderHeader {
    border: 1px solid #00f2ff;
    border-radius: 5px;
    background-color: #1a1a1a;
}

/* Text */
.stMarkdown, body {
    color: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "brain" not in st.session_state:
    st.session_state.brain = PersonalBrain()
    st.session_state.brain.log_session()
    st.session_state.memory = MemoryManager("memory.json")
    st.session_state.ollama = OllamaHandler({})
    st.session_state.current_personality = "quirky"
    st.session_state.chat_history = []
    st.session_state.voice_enabled = True
    st.session_state.voice_input = None
    
    # Initialize Gemini handler (primary) and fallback to Ollama
    try:
        from utils.gemini_handler import GeminiHandler
        st.session_state.gemini = GeminiHandler({})
    except Exception as e:
        print(f"Gemini handler initialization error: {e}")
        st.session_state.gemini = None
    
    # Initialize voice handler
    try:
        from utils.voice import VoiceHandler
        st.session_state.voice_handler = VoiceHandler({})
    except Exception as e:
        print(f"Voice handler initialization error: {e}")
        st.session_state.voice_handler = None

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 EVE Control Panel")
    
    # EVE Avatar with dynamic greeting
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Check if we have EVE's profile picture
        eve_image_path = Path(__file__).parent / "assets" / "eve_profile.jpg"
        if eve_image_path.exists():
            st.markdown(
                '<div style="text-align: center; position: relative;">',
                unsafe_allow_html=True
            )
            st.image(str(eve_image_path), width=140, use_container_width=False)
            st.markdown(
                '<h3 style="margin: 10px 0; color: #ff9d00;">EVE</h3><span class="status-online"></span> <small>ONLINE</small></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 60px; animation: float 3s ease-in-out infinite;">🤖</div>
                <h3 style="margin: 10px 0; color: #ff9d00;">EVE</h3>
                <span class="status-online"></span> <small>ONLINE</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Dynamic greeting based on session
    profile = st.session_state.brain.get_memory_summary()
    greeting = f"Welcome back, {profile['name']}! ✨" if profile['name'] != "Gemini" else f"Hey there! Ready to create? 🚀"
    st.success(greeting)
    
    st.divider()
    
    # Personality selector with visual feedback
    st.markdown("#### 🎭 Personality Mode")
    personality = st.selectbox(
        "Select personality:",
        options=list(PERSONALITY_DESCRIPTIONS.keys()),
        index=list(PERSONALITY_DESCRIPTIONS.keys()).index(st.session_state.current_personality),
        key="personality_select"
    )
    st.session_state.current_personality = personality
    
    # Show personality description with colored background
    st.info(f"💬 {PERSONALITY_DESCRIPTIONS[personality]}")
    
    st.divider()
    
    # Profile info with visual metrics
    st.markdown("#### 📊 Profile Overview")
    profile = st.session_state.brain.get_memory_summary()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🔄 Sessions", profile["sessions"])
        st.metric("📚 Learnings", profile["learnings"])
    with col2:
        st.metric("🚀 Projects", profile["projects"])
        st.metric("📈 Profile", f"{profile['profile_completeness']}%")
    
    # Visual progress bar
    progress_value = profile['profile_completeness'] / 100
    st.progress(progress_value, text=f"Profile Completeness: {profile['profile_completeness']}%")
    
    st.divider()
    
    # System status with visual indicators
    st.markdown("#### ⚙️ System Status")
    try:
        # Check Gemini status (primary)
        gemini_status = st.session_state.gemini and st.session_state.gemini.check_connection()
        if gemini_status:
            st.markdown('<span class="status-online"></span> **Gemini: ONLINE** (✨ Premium AI)', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-offline"></span> **Gemini: OFFLINE**', unsafe_allow_html=True)
        
        # Check Ollama status (fallback)
        ollama_status = st.session_state.ollama.check_connection()
        if ollama_status:
            st.markdown('<span class="status-online"></span> **Ollama: ONLINE** (Fallback)', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-offline"></span> **Ollama: OFFLINE**', unsafe_allow_html=True)
    except Exception as e:
        st.markdown('<span class="status-offline"></span> **AI Services: OFFLINE**', unsafe_allow_html=True)
    
    st.divider()
    
    # Voice control settings
    st.markdown("#### 🔊 Voice Control")
    
    voice_enabled = st.checkbox("🎤 Enable Voice Output", value=True)
    st.session_state.voice_enabled = voice_enabled
    
    if voice_enabled and hasattr(st.session_state, 'voice_handler') and st.session_state.voice_handler:
        # Voice selection
        st.markdown("**👩 Select EVE's Voice:**")
        try:
            available_voices = st.session_state.voice_handler.get_available_voices()
        except Exception as e:
            print(f"Error getting available voices: {e}")
            available_voices = []
        
        if available_voices:
            # Separate female and other voices
            female_voices = [v for v in available_voices if v['is_female']]
            other_voices = [v for v in available_voices if not v['is_female']]
            
            voice_options = []
            voice_ids = []
            
            # Build voice options list (no markdown during building)
            for voice in female_voices:
                voice_options.append(f"👩 {voice['name']}")
                voice_ids.append(voice['id'])
            
            for voice in other_voices:
                voice_options.append(f"🎙️ {voice['name']}")
                voice_ids.append(voice['id'])
            
            if voice_options:
                selected_voice_idx = st.selectbox(
                    "Choose voice:",
                    range(len(voice_options)),
                    format_func=lambda x: voice_options[x],
                    key="voice_select"
                )
                try:
                    st.session_state.voice_handler.set_voice(voice_ids[selected_voice_idx])
                except Exception as e:
                    print(f"Error setting voice: {e}")
            else:
                st.warning("No voices available")
        else:
            st.info("Voice selection not available")
        
        # Voice properties sliders
        try:
            voice_speed = st.slider("Speech Speed", 50, 300, 150, 10)
            st.session_state.voice_handler.set_voice_rate(voice_speed)
            
            voice_volume = st.slider("Volume", 0.0, 1.0, 0.9, 0.1)
            st.session_state.voice_handler.set_voice_volume(voice_volume)
        except Exception as e:
            print(f"Error setting voice properties: {e}")
        
        # Test voice button
        if st.button("🔊 Test Voice", use_container_width=True):
            try:
                st.session_state.voice_handler.speak("Hello! I am EVE, your AI companion. I can now speak to you!")
                st.success("✓ Voice test playing...")
            except Exception as e:
                print(f"Error during test voice: {e}")
                st.error(f"Voice test failed: {e}")

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "📚 Profile", "🎓 Learning", "📁 Projects", "💾 Memory"])

# TAB 1: CHAT
with tab1:
    st.markdown("## 💬 Chat with EVE")
    st.markdown("---")
    
    # Display chat history with animations
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**You:** {msg['content']}")
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**EVE:** {msg['content']}")
                # Add subtle glow effect
                st.markdown("""
                <style>
                .stChatMessage:last-child {
                    animation: fadeIn 0.8s ease-in;
                }
                </style>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Voice & Text input section with visual separation
    st.markdown("### 🎤 Your Input")
    
    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        st.markdown("**🎙️ Voice**")
        st.markdown("<small>Click to record your voice</small>", unsafe_allow_html=True)
        audio_data = st.audio_input("Record message", label_visibility="collapsed")
        
        # Process audio if provided
        transcribed_text = None
        if audio_data is not None:
            with st.spinner("🎧 Transcribing audio..."):
                try:
                    import tempfile
                    import os
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(audio_data.getbuffer())
                        tmp_path = tmp_file.name
                    
                    if hasattr(st.session_state, 'voice_handler') and st.session_state.voice_handler:
                        result = st.session_state.voice_handler.transcribe_file(tmp_path)
                        transcribed_text = result if result else None
                    
                    os.unlink(tmp_path)
                except Exception as e:
                    st.error(f"Voice transcription not available: {str(e)}")
            
            # Show transcribed text with preview + action buttons
            if transcribed_text:
                st.markdown("#### 📝 Transcribed Text")
                st.info(transcribed_text)
                
                col_accept, col_discard = st.columns(2)
                with col_accept:
                    if st.button("✅ Send", use_container_width=True, key="voice_send"):
                        st.session_state.voice_input = transcribed_text
                        st.rerun()  # Rerun to process the message
                
                with col_discard:
                    if st.button("❌ Discard", use_container_width=True, key="voice_discard"):
                        st.rerun()  # Rerun to clear and show fresh input
    
    with col2:
        st.markdown("**⌨️ Text**")
        st.markdown("<small>Or type your message</small>", unsafe_allow_html=True)
        text_input = st.chat_input("Ask EVE something...", key="chat_input")
        
        # Use voice input if available (from voice preview Send button)
        if hasattr(st.session_state, 'voice_input') and st.session_state.voice_input:
            user_input = st.session_state.voice_input
            st.session_state.voice_input = None  # Clear it after using
        else:
            user_input = text_input
    
    if user_input:
        # Add user message with animation
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.markdown(f"**You:** {user_input}")
        
        # EVE is thinking animation
        thinking_placeholder = st.empty()
        with thinking_placeholder.container():
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 40px; animation: float 0.8s ease-in-out infinite;">🧠</div>
                <p style="color: #00f2ff; animation: glow 2s ease-in-out infinite;">EVE is thinking...</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Get EVE response with streaming enabled
        try:
            # Build context-aware prompt with recent memory
            system_prompt = st.session_state.brain.get_system_prompt_for_personality(
                st.session_state.current_personality
            )
            
            # Build context from recent conversation history (last 10 messages for longer memory)
            recent_context = ""
            if st.session_state.chat_history:
                recent_messages = st.session_state.chat_history[-10:]  # Last 10 messages
                for msg in recent_messages:
                    role = "You" if msg["role"] == "user" else "EVE"
                    recent_context += f"{role}: {msg['content']}\n"
            
            # Construct full prompt with context
            full_prompt = f"{system_prompt}\n\n"
            if recent_context:
                full_prompt += f"Recent conversation:\n{recent_context}\n"
            full_prompt += f"User: {user_input}\n\nEVE:"
            
            thinking_placeholder.empty()
            
            # Show EVE response with streaming (real-time text update)
            with st.chat_message("assistant", avatar="🤖"):
                response_placeholder = st.empty()
                response_parts = []  # Use list to hold streamed text
                
                # Use Gemini if available, fallback to Ollama
                if st.session_state.gemini and st.session_state.gemini.check_connection():
                    # Stream from Gemini
                    def stream_callback(chunk):
                        response_parts.append(chunk)
                        current_text = "".join(response_parts)
                        response_placeholder.markdown(f"**EVE:** {current_text}")
                    
                    response = st.session_state.gemini.generate(
                        full_prompt,
                        stream=True,
                        callback=stream_callback
                    )
                    response_text = "".join(response_parts)
                else:
                    # Fallback to Ollama
                    response = st.session_state.ollama.generate(
                        full_prompt,
                        stream=True
                    )
                    response_text = response
                    response_placeholder.markdown(f"**EVE:** {response_text}")
                
                # Clean response
                response_text = response_text.strip()
                if response_text.startswith("EVE:"):
                    response_text = response_text[4:].strip()
                
                # Final display with animation
                response_placeholder.markdown(f"**EVE:** {response_text}")
                st.markdown("""
                <style>
                .stChatMessage:last-child {
                    animation: fadeIn 0.8s ease-in;
                    border-color: #ff9d00;
                }
                </style>
                """, unsafe_allow_html=True)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            
            # EVE speaks the response asynchronously (if enabled)
            if st.session_state.get('voice_enabled', True):
                if hasattr(st.session_state, 'voice_handler') and st.session_state.voice_handler:
                    st.session_state.voice_handler.speak_async(response_text)
            
            # Store in memory
            st.session_state.memory.add_conversation("user", user_input)
            st.session_state.memory.add_conversation("assistant", response_text)
            
            # Success feedback with animation
            st.balloons()
            
        except Exception as e:
            thinking_placeholder.empty()
            error_msg = f"❌ Error: {str(e)}"
            st.error(error_msg)
            response_text = f"Sorry, I'm having trouble connecting to my brain!"
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            print(f"Full error: {e}")
            import traceback
            traceback.print_exc()

# TAB 2: PROFILE
with tab2:
    st.markdown("## 📊 Your Profile")
    
    # Display profile picture if available
    user_image_path = Path(__file__).parent / "assets" / "user_profile.jpg"
    if user_image_path.exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align: center; margin-bottom: 20px;">',
                unsafe_allow_html=True
            )
            st.image(str(user_image_path), width=180, use_container_width=False)
            st.markdown('</div>', unsafe_allow_html=True)
    
    profile = st.session_state.brain.get_memory_summary()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Name", profile["name"])
        st.metric("Sessions", profile["sessions"])
        st.metric("Completeness", f"{profile['profile_completeness']}%")
    
    with col2:
        st.metric("Projects", profile["projects"])
        st.metric("Learnings", profile["learnings"])
        st.metric("Skills", len(profile.get("interests", [])))
    
    st.divider()
    
    # Show interests if available
    if hasattr(st.session_state.brain, 'interests') and st.session_state.brain.interests:
        st.markdown("### 🎯 Active Interests")
        active = [k for k, v in st.session_state.brain.interests.items() if v]
        if active:
            cols = st.columns(3)
            for i, interest in enumerate(active):
                with cols[i % 3]:
                    st.info(f"✓ {interest.replace('_', ' ').title()}")
    
    # Astrological profile if available
    if hasattr(st.session_state.brain, 'data') and 'astrological_profile' in st.session_state.brain.data:
        st.markdown("### 🌙 Astrological Profile")
        astro = st.session_state.brain.data['astrological_profile']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"☀️ Sun: {astro.get('sun_sign', 'Unknown')}")
        with col2:
            st.info(f"🌙 Moon: {astro.get('moon_sign', 'Unknown')}")
        with col3:
            st.info(f"⬆️ Ascendant: {astro.get('ascendant', 'Unknown')}")

# TAB 3: LEARNING
with tab3:
    st.markdown("## 🎓 Add Learning")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Learning Topic", placeholder="e.g., Python async/await patterns")
    with col2:
        context = st.selectbox("Context", ["General", "Work", "Personal", "Technical"])
    
    insight = st.text_area("Insight", placeholder="What did you learn?", height=120)
    
    if st.button("💾 Store Learning", type="primary"):
        if topic and insight:
            st.session_state.brain.store_learning(topic, insight, context)
            st.success(f"✅ Stored learning: {topic}")
            st.balloons()
        else:
            st.warning("Please fill in both topic and insight")
    
    st.divider()
    
    # Display recent learnings
    if st.session_state.brain.learning_history:
        st.markdown("### 📖 Recent Learnings")
        for i, learning in enumerate(reversed(st.session_state.brain.learning_history[-5:])):
            with st.expander(f"📚 {learning['topic']}"):
                st.markdown(f"**Insight:** {learning['insight']}")
                st.caption(f"Context: {learning.get('context', 'General')}")

# TAB 4: PROJECTS
with tab4:
    st.markdown("## 📁 Your Projects")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        project_name = st.text_input("Project Name", placeholder="e.g., EVE AI Assistant")
    with col2:
        language = st.selectbox("Language", ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Other"])
    
    description = st.text_area("Description", placeholder="What's this project about?", height=100)
    
    tags = st.multiselect(
        "Tags",
        ["AI", "Web", "Desktop", "CLI", "Game", "Library", "Tool", "Learning", "Hobby"]
    )
    
    if st.button("🚀 Add Project", type="primary"):
        if project_name and description:
            st.session_state.brain.store_project(project_name, description, language, tags)
            st.success(f"✅ Project added: {project_name}")
            st.balloons()
        else:
            st.warning("Please fill in project name and description")
    
    st.divider()
    
    # Display projects
    if st.session_state.brain.past_projects:
        st.markdown("### 🎯 Your Projects")
        for project in st.session_state.brain.past_projects:
            with st.expander(f"🚀 {project['name']} ({project['language']})"):
                st.markdown(project['description'])
                if project.get('tags'):
                    tags_str = " | ".join([f"🏷️ {tag}" for tag in project['tags']])
                    st.caption(tags_str)

# TAB 5: MEMORY
with tab5:
    st.markdown("## 💾 Memory & Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Profile (JSON)", type="secondary"):
            profile_json = json.dumps(st.session_state.brain.data, indent=2)
            st.download_button(
                label="Download Profile",
                data=profile_json,
                file_name="eve_profile.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    st.divider()
    
    # Memory stats
    st.markdown("### 📊 Memory Statistics")
    
    profile_data = st.session_state.brain.get_memory_summary()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Chat Messages", len(st.session_state.chat_history))
    with col2:
        st.metric("Stored Learnings", profile_data.get("learnings", 0))
    with col3:
        st.metric("Projects", profile_data.get("projects", 0))
    
    st.divider()
    
    # Raw data viewer
    if st.checkbox("👁️ View Raw Profile Data"):
        st.json(st.session_state.brain.data)
    
    if st.checkbox("👁️ View Chat History"):
        st.json(st.session_state.chat_history)

# Footer
st.divider()
st.markdown("""
---
**EVE** - Your AI Partner in Creation  
🧠 Powered by PersonalBrain + Ollama  
🎨 Cyberpunk UI | 🔐 Local-First AI
""")
