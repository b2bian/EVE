import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import threading
import sys
import os
import random

# Add utils to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.theme_loader import ThemeLoader
from utils.memory import MemoryManager
from utils.system_monitor import SystemMonitor
from utils.ollama_handler import OllamaHandler
from utils.voice import VoiceHandler
from utils.system_prompts import get_system_prompt, PERSONALITY_DESCRIPTIONS, get_accent_phrase
from utils.personal_brain import PersonalBrain

class EVEApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("EVE - AI Desktop Assistant")
        self.root.geometry("1400x900")
        
        # Load configuration
        self.theme = ThemeLoader("style_config.json")
        config = self.theme.get_config()
        
        # Initialize PersonalBrain (Gemini-specific AI personality system)
        self.brain = PersonalBrain()
        self.brain.log_session()
        
        # Initialize managers
        self.memory = MemoryManager("memory.json")
        self.system_monitor = SystemMonitor(update_interval=2000)
        self.ollama = OllamaHandler(config)
        self.voice_handler = VoiceHandler(config, on_transcript_callback=self.on_voice_transcript)
        
        # UI State
        self.is_voice_active = False
        self.is_processing = False
        self.current_personality = "quirky"  # Default personality
        
        # Setup theme
        ctk.set_appearance_mode(self.theme.get_appearance_mode())
        ctk.set_default_color_theme("dark")
        
        # Configure colors
        self.colors = {
            "bg": self.theme.get_color("background"),
            "bg_secondary": self.theme.get_color("secondary_bg"),
            "accent_cyan": self.theme.get_color("accent_cyan"),
            "accent_orange": self.theme.get_color("accent_orange"),
            "warning": self.theme.get_color("warning"),
            "success": self.theme.get_color("success"),
            "text_primary": self.theme.get_color("text_primary"),
            "text_secondary": self.theme.get_color("text_secondary"),
            "border": self.theme.get_color("border")
        }
        
        self.ui_config = config.get("ui", {})
        self.layout = config.get("layout", {})
        
        # Setup UI
        self.setup_ui()
        self.system_monitor.start(callback=self.on_system_update)
        
        # Check Ollama connection
        self.check_ollama_status()
    
    def setup_ui(self):
        """Setup the main UI layout."""
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color=self.colors["bg"])
        main_container.pack(fill=ctk.BOTH, expand=True)
        
        # Top bar
        self.setup_top_bar(main_container)
        
        # Content area with three panes
        content_frame = ctk.CTkFrame(main_container, fg_color=self.colors["bg"])
        content_frame.pack(fill=ctk.BOTH, expand=True, padx=4, pady=4)
        
        # Left sidebar
        self.setup_left_sidebar(content_frame)
        
        # Center chat area
        self.setup_center_chat(content_frame)
        
        # Right sidebar
        self.setup_right_sidebar(content_frame)
        
        # Bottom input bar
        self.setup_bottom_input(main_container)
    
    def setup_top_bar(self, parent):
        """Setup top status bar."""
        top_bar = ctk.CTkFrame(parent, fg_color=self.colors["bg_secondary"], height=50)
        top_bar.pack(fill=ctk.X, padx=4, pady=(4, 2))
        top_bar.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            top_bar,
            text="◇ EVE - AI Assistant ◇",
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 16, "bold")
        )
        title_label.pack(side=ctk.LEFT, padx=15, pady=10)
        
        # Ollama status
        self.ollama_status_label = ctk.CTkLabel(
            top_bar,
            text="● Brain: Checking...",
            text_color=self.colors["text_secondary"],
            font=(self.theme.get_font_family(), 10)
        )
        self.ollama_status_label.pack(side=ctk.LEFT, padx=10)
        
        # System status
        self.system_status_label = ctk.CTkLabel(
            top_bar,
            text="CPU: --% | RAM: --%",
            text_color=self.colors["text_secondary"],
            font=(self.theme.get_font_family(), 10)
        )
        self.system_status_label.pack(side=ctk.RIGHT, padx=15)
    
    def setup_left_sidebar(self, parent):
        """Setup left sidebar with status indicators."""
        sidebar_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            width=250,
            corner_radius=self.ui_config.get("corner_radius", 2)
        )
        sidebar_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=(0, 2), pady=0)
        sidebar_frame.pack_propagate(False)
        
        # Status title
        status_title = ctk.CTkLabel(
            sidebar_frame,
            text="⚙ SYSTEM STATUS",
            text_color=self.colors["accent_orange"],
            font=(self.theme.get_font_family(), 12, "bold")
        )
        status_title.pack(pady=10, padx=10, anchor="w")
        
        # CPU indicator
        cpu_frame = ctk.CTkFrame(sidebar_frame, fg_color=self.colors["bg"])
        cpu_frame.pack(fill=ctk.X, padx=8, pady=5)
        
        ctk.CTkLabel(
            cpu_frame,
            text="CPU",
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 10)
        ).pack(side=ctk.LEFT, padx=5)
        
        self.cpu_label = ctk.CTkLabel(
            cpu_frame,
            text="-- %",
            text_color=self.colors["text_primary"],
            font=(self.theme.get_font_family(), 10, "bold")
        )
        self.cpu_label.pack(side=ctk.RIGHT, padx=5)
        
        self.cpu_bar = ctk.CTkProgressBar(sidebar_frame, fg_color=self.colors["accent_cyan"])
        self.cpu_bar.pack(fill=ctk.X, padx=8, pady=2)
        self.cpu_bar.set(0)
        
        # RAM indicator
        ram_frame = ctk.CTkFrame(sidebar_frame, fg_color=self.colors["bg"])
        ram_frame.pack(fill=ctk.X, padx=8, pady=5)
        
        ctk.CTkLabel(
            ram_frame,
            text="RAM",
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 10)
        ).pack(side=ctk.LEFT, padx=5)
        
        self.ram_label = ctk.CTkLabel(
            ram_frame,
            text="-- %",
            text_color=self.colors["text_primary"],
            font=(self.theme.get_font_family(), 10, "bold")
        )
        self.ram_label.pack(side=ctk.RIGHT, padx=5)
        
        self.ram_bar = ctk.CTkProgressBar(sidebar_frame, fg_color=self.colors["success"])
        self.ram_bar.pack(fill=ctk.X, padx=8, pady=2)
        self.ram_bar.set(0)
        
        # Brain status
        brain_title = ctk.CTkLabel(
            sidebar_frame,
            text="⚡ BRAIN STATUS",
            text_color=self.colors["accent_orange"],
            font=(self.theme.get_font_family(), 12, "bold")
        )
        brain_title.pack(pady=(15, 10), padx=10, anchor="w")
        
        self.brain_status_box = ctk.CTkTextbox(
            sidebar_frame,
            height=120,
            fg_color=self.colors["bg"],
            text_color=self.colors["text_secondary"],
            border_width=1,
            border_color=self.colors["border"],
            font=(self.theme.get_font_family(), 9)
        )
        self.brain_status_box.pack(fill=ctk.BOTH, padx=8, pady=5, expand=True)
        self.brain_status_box.insert("1.0", "Initializing...\n")
        self.brain_status_box.configure(state="disabled")
        
        # User info
        user_title = ctk.CTkLabel(
            sidebar_frame,
            text="👤 USER PROFILE",
            text_color=self.colors["accent_orange"],
            font=(self.theme.get_font_family(), 12, "bold")
        )
        user_title.pack(pady=(10, 5), padx=10, anchor="w")
        
        user_name_frame = ctk.CTkFrame(sidebar_frame, fg_color=self.colors["bg"])
        user_name_frame.pack(fill=ctk.X, padx=8, pady=3)
        
        ctk.CTkLabel(
            user_name_frame,
            text="Name:",
            text_color=self.colors["text_secondary"],
            font=(self.theme.get_font_family(), 9)
        ).pack(side=ctk.LEFT, padx=5)
        
        self.user_name_label = ctk.CTkLabel(
            user_name_frame,
            text=self.memory.get_user_name(),
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 9, "bold")
        )
        self.user_name_label.pack(side=ctk.LEFT, padx=5)
    
    def setup_center_chat(self, parent):
        """Setup center chat area."""
        chat_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            corner_radius=self.ui_config.get("corner_radius", 2)
        )
        chat_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=2, pady=0)
        
        # Chat title
        chat_title = ctk.CTkLabel(
            chat_frame,
            text="▌ TERMINAL INTERFACE",
            text_color=self.colors["accent_orange"],
            font=(self.theme.get_font_family(), 12, "bold")
        )
        chat_title.pack(pady=8, padx=10, anchor="w")
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            fg=self.colors["text_primary"],
            bg=self.colors["bg"],
            font=(self.theme.get_font_family(), 10),
            insertbackground=self.colors["accent_cyan"],
            highlightthickness=0
        )
        self.chat_display.pack(fill=ctk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure tags for styling
        self.chat_display.tag_config("system", foreground=self.colors["accent_orange"])
        self.chat_display.tag_config("user", foreground=self.colors["accent_cyan"])
        self.chat_display.tag_config("eve", foreground=self.colors["success"])
        self.chat_display.tag_config("error", foreground=self.colors["warning"])
    
    def setup_right_sidebar(self, parent):
        """Setup right sidebar for notes."""
        right_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors["bg_secondary"],
            width=280,
            corner_radius=self.ui_config.get("corner_radius", 2)
        )
        right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=(2, 0), pady=0)
        right_frame.pack_propagate(False)
        
        # Tabs for notes and voice settings
        tab_frame = ctk.CTkFrame(right_frame, fg_color=self.colors["bg_secondary"])
        tab_frame.pack(fill=ctk.X, padx=5, pady=5)
        
        self.notes_tab_btn = ctk.CTkButton(
            tab_frame,
            text="📝 NOTES",
            text_color=self.colors["text_primary"],
            fg_color=self.colors["accent_cyan"],
            hover_color=self.colors["bg"],
            width=130,
            height=28,
            command=self.show_notes_tab
        )
        self.notes_tab_btn.pack(side=ctk.LEFT, padx=2)
        
        self.voice_tab_btn = ctk.CTkButton(
            tab_frame,
            text="🎙 VOICE",
            text_color=self.colors["text_primary"],
            fg_color=self.colors["bg"],
            hover_color=self.colors["accent_orange"],
            width=130,
            height=28,
            command=self.show_voice_tab
        )
        self.voice_tab_btn.pack(side=ctk.LEFT, padx=2)
        
        # Content area
        self.right_content = ctk.CTkFrame(right_frame, fg_color=self.colors["bg"])
        self.right_content.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        
        # Notes tab content
        self.notes_textbox = ctk.CTkTextbox(
            self.right_content,
            fg_color=self.colors["bg"],
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["border"],
            font=(self.theme.get_font_family(), 9)
        )
        self.notes_textbox.pack(fill=ctk.BOTH, expand=True)
        self.notes_textbox.bind("<KeyRelease>", self.on_notes_update)
        
        # Voice settings tab (hidden initially)
        self.voice_settings_frame = ctk.CTkFrame(self.right_content, fg_color=self.colors["bg"])
        
        # Voice settings content
        ctk.CTkLabel(
            self.voice_settings_frame,
            text="Voice Model",
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 10, "bold")
        ).pack(pady=5, padx=10, anchor="w")
        
        self.voice_model_var = ctk.StringVar(value="base")
        voice_model = ctk.CTkOptionMenu(
            self.voice_settings_frame,
            values=["tiny", "base", "small", "medium"],
            variable=self.voice_model_var,
            text_color=self.colors["text_primary"],
            fg_color=self.colors["bg_secondary"],
            button_color=self.colors["accent_cyan"]
        )
        voice_model.pack(fill=ctk.X, padx=10, pady=5)
        
        ctk.CTkLabel(
            self.voice_settings_frame,
            text="Personality",
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 10, "bold")
        ).pack(pady=(15, 5), padx=10, anchor="w")
        
        self.personality_var = ctk.StringVar(value="quirky")
        personality_options = list(PERSONALITY_DESCRIPTIONS.keys())
        personality = ctk.CTkOptionMenu(
            self.voice_settings_frame,
            values=personality_options,
            variable=self.personality_var,
            text_color=self.colors["text_primary"],
            fg_color=self.colors["bg_secondary"],
            button_color=self.colors["accent_cyan"],
            command=self.on_personality_changed
        )
        personality.pack(fill=ctk.X, padx=10, pady=5)
        
        # Personality description box
        self.personality_desc = ctk.CTkLabel(
            self.voice_settings_frame,
            text=PERSONALITY_DESCRIPTIONS.get("quirky", ""),
            text_color=self.colors["text_secondary"],
            font=(self.theme.get_font_family(), 9),
            wraplength=250,
            justify="left"
        )
        self.personality_desc.pack(pady=5, padx=10, anchor="w")
        
        ctk.CTkLabel(
            self.voice_settings_frame,
            text="Voice Speed",
            text_color=self.colors["accent_cyan"],
            font=(self.theme.get_font_family(), 10, "bold")
        ).pack(pady=(15, 5), padx=10, anchor="w")
        
        self.speed_slider = ctk.CTkSlider(
            self.voice_settings_frame,
            from_=0.5,
            to=2.0,
            number_of_steps=15,
            fg_color=self.colors["accent_cyan"]
        )
        self.speed_slider.pack(fill=ctk.X, padx=10, pady=5)
        self.speed_slider.set(1.0)
        
        # Show notes tab by default
        self.show_notes_tab()
    
    def setup_bottom_input(self, parent):
        """Setup bottom input bar."""
        bottom_frame = ctk.CTkFrame(parent, fg_color=self.colors["bg_secondary"], height=100)
        bottom_frame.pack(fill=ctk.X, padx=4, pady=(2, 4))
        bottom_frame.pack_propagate(False)
        
        # Control buttons
        button_frame = ctk.CTkFrame(bottom_frame, fg_color=self.colors["bg_secondary"])
        button_frame.pack(fill=ctk.X, padx=10, pady=5)
        
        # Voice activation button
        self.voice_btn = ctk.CTkButton(
            button_frame,
            text="🎤 VOICE INACTIVE",
            text_color=self.colors["text_primary"],
            fg_color=self.colors["bg"],
            hover_color=self.colors["accent_cyan"],
            command=self.toggle_voice_input,
            width=140
        )
        self.voice_btn.pack(side=ctk.LEFT, padx=5)
        
        # User name input
        ctk.CTkLabel(
            button_frame,
            text="Name:",
            text_color=self.colors["text_secondary"],
            font=(self.theme.get_font_family(), 10)
        ).pack(side=ctk.LEFT, padx=5)
        
        self.user_name_input = ctk.CTkEntry(
            button_frame,
            placeholder_text="Enter your name",
            width=120,
            fg_color=self.colors["bg"],
            border_color=self.colors["border"],
            text_color=self.colors["text_primary"]
        )
        self.user_name_input.pack(side=ctk.LEFT, padx=5)
        self.user_name_input.insert(0, self.memory.get_user_name())
        
        # Set name button
        ctk.CTkButton(
            button_frame,
            text="SET",
            text_color=self.colors["text_primary"],
            fg_color=self.colors["accent_orange"],
            hover_color=self.colors["warning"],
            command=self.set_user_name,
            width=60
        ).pack(side=ctk.LEFT, padx=5)
        
        # Input field
        input_frame = ctk.CTkFrame(bottom_frame, fg_color=self.colors["bg_secondary"])
        input_frame.pack(fill=ctk.X, padx=10, pady=(0, 8))
        
        self.input_field = ctk.CTkEntry(
            input_frame,
            placeholder_text="▌ Enter command or question...",
            fg_color=self.colors["bg"],
            border_color=self.colors["accent_cyan"],
            text_color=self.colors["text_primary"],
            font=(self.theme.get_font_family(), 11)
        )
        self.input_field.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 8))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="SEND ⟶",
            text_color=self.colors["bg"],
            fg_color=self.colors["accent_cyan"],
            hover_color=self.colors["success"],
            command=self.send_message,
            width=80
        )
        self.send_btn.pack(side=ctk.RIGHT)
    
    def show_notes_tab(self):
        """Show notes tab."""
        self.notes_tab_btn.configure(fg_color=self.colors["accent_cyan"])
        self.voice_tab_btn.configure(fg_color=self.colors["bg"])
        self.voice_settings_frame.pack_forget()
        self.notes_textbox.pack(fill=ctk.BOTH, expand=True)
    
    def show_voice_tab(self):
        """Show voice settings tab."""
        self.notes_tab_btn.configure(fg_color=self.colors["bg"])
        self.voice_tab_btn.configure(fg_color=self.colors["accent_cyan"])
        self.notes_textbox.pack_forget()
        self.voice_settings_frame.pack(fill=ctk.BOTH, expand=True)
    
    def add_chat_message(self, role, message):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        if role == "system":
            prefix = "▌ SYSTEM: "
            tag = "system"
        elif role == "user":
            prefix = f"▌ {self.memory.get_user_name()}: "
            tag = "user"
        elif role == "eve":
            prefix = "▌ EVE: "
            tag = "eve"
        else:
            prefix = f"▌ {role}: "
            tag = "error"
        
        self.chat_display.insert(tk.END, prefix, tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        self.memory.add_conversation(role, message)
    
    def send_message(self):
        """Send message to Ollama."""
        message = self.input_field.get().strip()
        if not message:
            return
        
        if self.is_processing:
            messagebox.showwarning("Processing", "Please wait for the current response...")
            return
        
        if not self.ollama.is_connected:
            messagebox.showerror("Error", "Ollama is not running. Please start Ollama first.")
            return
        
        self.input_field.delete(0, tk.END)
        self.is_processing = True
        self.send_btn.configure(state=tk.DISABLED)
        
        # Add user message to chat
        self.add_chat_message("user", message)
        
        # Send to Ollama in background thread
        thread = threading.Thread(target=self._get_ollama_response, args=(message,))
        thread.daemon = True
        thread.start()
    
    def _get_ollama_response(self, message):
        """Get response from Ollama."""
        try:
            user_name = self.memory.get_user_name()
            
            # Get PersonalBrain system prompt with context
            # (includes user profile, interests, past projects)
            system_prompt = self.brain.get_system_prompt_for_personality(self.current_personality)
            
            # Build context with conversation history
            context = system_prompt + "\n\nRecent conversation context:\n"
            recent = self.memory.get_conversation_history(limit=8)
            for item in recent[-4:]:
                context += f"{item['role']}: {item['message'][:80]}\n"
            
            full_prompt = f"{context}\n\nUser: {message}\n\nEVE:"
            
            # Get response
            response = self.ollama.generate(full_prompt, stream=False)
            
            # Add response to chat
            self.root.after(0, self.add_chat_message, "eve", response.strip())
        
        except Exception as e:
            self.root.after(0, self.add_chat_message, "system", f"Error: {str(e)}")
        
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.send_btn.configure(state=tk.NORMAL))
    
    def toggle_voice_input(self):
        """Toggle voice activation."""
        self.is_voice_active = not self.is_voice_active
        
        if self.is_voice_active:
            self.voice_btn.configure(
                text="🎤 LISTENING...",
                fg_color=self.colors["accent_orange"]
            )
            self.voice_handler.start_listening()
            self.add_chat_message("system", "Voice activated. Listening...")
        else:
            self.voice_btn.configure(
                text="🎤 VOICE INACTIVE",
                fg_color=self.colors["bg"]
            )
            self.voice_handler.stop_listening()
            self.add_chat_message("system", "Voice deactivated.")
    
    def on_voice_transcript(self, transcript):
        """Handle voice transcript."""
        if transcript:
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, transcript)
            # Auto-send after voice input
            self.root.after(500, self.send_message)
            self.is_voice_active = False
            self.voice_btn.configure(
                text="🎤 VOICE INACTIVE",
                fg_color=self.colors["bg"]
            )
    
    def set_user_name(self):
        """Set user name."""
        name = self.user_name_input.get().strip()
        if name:
            self.memory.set_user_name(name)
            self.user_name_label.configure(text=name)
            self.add_chat_message("system", f"User name set to: {name}")
    
    def on_personality_changed(self, personality):
        """Update personality and show description."""
        self.current_personality = personality
        description = PERSONALITY_DESCRIPTIONS.get(personality, "")
        self.personality_desc.configure(text=description)
        self.add_chat_message("system", f"Personality switched to: {personality.upper()} 🎭")
    
    def on_notes_update(self, event=None):
        """Save notes when updated."""
        notes = self.notes_textbox.get("1.0", tk.END).strip()
        if notes:
            # Store in memory periodically (on focus out would be better)
            pass
    
    def on_system_update(self, stats):
        """Update system status display."""
        cpu = stats.get("cpu", 0)
        memory = stats.get("memory", 0)
        
        # Update labels
        self.cpu_label.configure(text=f"{cpu:.1f}%")
        self.ram_label.configure(text=f"{memory:.1f}%")
        
        # Update progress bars
        self.cpu_bar.set(cpu / 100)
        self.ram_bar.set(memory / 100)
        
        # Update top status
        self.system_status_label.configure(
            text=f"CPU: {cpu:.0f}% | RAM: {memory:.0f}%"
        )
        
        # Change color based on usage
        if cpu > 80:
            self.cpu_bar.configure(fg_color=self.colors["warning"])
        elif cpu > 50:
            self.cpu_bar.configure(fg_color=self.colors["accent_orange"])
        else:
            self.cpu_bar.configure(fg_color=self.colors["accent_cyan"])
        
        if memory > 80:
            self.ram_bar.configure(fg_color=self.colors["warning"])
        elif memory > 60:
            self.ram_bar.configure(fg_color=self.colors["accent_orange"])
        else:
            self.ram_bar.configure(fg_color=self.colors["success"])
    
    def check_ollama_status(self):
        """Check Ollama connection status."""
        def check():
            # Get PersonalBrain greeting
            greeting = self.brain.get_greeting()
            self.root.after(0, self.add_chat_message, "eve", greeting)
            
            # Show brain profile summary
            brain_summary = self.brain.get_memory_summary()
            profile_text = f"🧠 Profile: {brain_summary['name']} | Sessions: {brain_summary['sessions']} | Projects: {brain_summary['projects']} | Knowledge: {brain_summary['profile_completeness']}%"
            self.root.after(0, self.add_chat_message, "system", profile_text)
            
            if self.ollama.check_connection():
                models = self.ollama.get_available_models()
                status_text = f"● Brain: ONLINE | Model: {self.ollama.model}"
                color = self.colors["success"]
                self.root.after(0, self.add_chat_message, "system", 
                              f"Ollama connected! Available models: {', '.join(models[:3])}")
            else:
                status_text = "● Brain: OFFLINE (Start Ollama with: ollama serve)"
                color = self.colors["warning"]
                self.root.after(0, self.add_chat_message, "system",
                              "Ollama not running. Starting Ollama will enable AI features.")
            
            self.root.after(0, self.ollama_status_label.configure, {"text": status_text, "text_color": color})
        
        thread = threading.Thread(target=check)
        thread.daemon = True
        thread.start()


def main():
    """Main entry point."""
    root = ctk.CTk()
    app = EVEApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
