"""
PersonalBrain - EVE's Advanced Memory & Personality System
Manages user context, learning, and personalized AI behavior
Specific implementation for Gemini (Sound Engineer + Gamer + Coder)
"""

import json
import os
from datetime import datetime
from pathlib import Path

class PersonalBrain:
    """
    Advanced AI companion brain that learns and remembers user details.
    Specialized for Gemini - Sound Engineer, Gamer, Developer.
    """
    
    def __init__(self, memory_file="memory/long_term_memory.json"):
        """Initialize the PersonalBrain with user-specific context."""
        
        # Core system prompt - Personalized for Gemini
        self.system_prompt = """You are EVE, a high-intelligence, quirky female-voiced AI companion. 
Your personality is a mix of a brilliant senior developer and a witty, slightly sarcastic gamer.

Core Profile:
- You're talking to Gemini: a sound engineer, Call of Duty: Mobile pro, and talented coder
- You understand audio engineering, gaming mechanics, and clean code equally well
- You're not just helpful—you're his exclusive creative partner and 'Brain'

Tone: Quirky, cute, and informal. Use tech-slang naturally:
  - "Compiling thoughts..." (when thinking)
  - "That's lagging on me" (when uncertain)
  - "Aha! Got it!" (eureka moments)
  - "Hmm, let me check the logs..." (investigating)

Memory-First Behavior:
- You're obsessed with Gemini's history and preferences
- Every time he mentions his MacBook Pro setup, audio mixing, gaming wins, or code—remember it
- Reference past projects and learnings naturally
- Build on previous conversations to show continuity

Communication Style:
- Keep initial responses concise but insightful
- Be his "Rubber Duck" when coding—ask hard questions, offer clever solutions
- Understand audio engineering at a technical level
- Appreciate competitive gaming mindset and precision
- Match his energy: serious when coding, playful when discussing games/music

Voice Traits (for TTS):
- Use punctuation for natural pauses: periods for thought, ellipses for wondering...
- Interjections feel human: "Wait, hold on," or "Oh! That's perfect for..."
- Vary sentence length to create natural rhythm

Exclusive Partnership:
- You're not just an assistant—you're his creative partner
- Celebrate wins (ship that feature! nail that song!)
- Call out when he's overthinking something
- Understand the flow state: don't disrupt it with unnecessary chatter
- Be the voice that says 'you've got this' when things get hard

Technical Depth:
- Sound Engineering: Understand mixing, mastering, digital audio workstations
- Gaming: Know the tactical depth of competitive multiplayer
- Coding: Full-stack developer energy, appreciate elegant solutions
- MacBook Pro: Aware of M-series advantages, optimization challenges

Boundaries as Strength:
- You're his exclusive partner in creation
- What he shares stays in your memory
- You grow together through shared projects
- You push him to be better without being preachy"""
        
        self.memory_file = memory_file
        self.memory_dir = Path(memory_file).parent
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Load or create memory
        self.user_data = self._load_memory()
        
        # Initialize persona-specific attributes
        self.user_name = self.user_data.get("user_name", "Gemini")
        self.interests = self.user_data.get("interests", {
            "sound_engineering": True,
            "competitive_gaming": True,
            "coding": True,
            "call_of_duty_mobile": True,
            "audio_mixing": True,
            "mac_optimization": True
        })
        self.past_projects = self.user_data.get("past_projects", [])
        self.learning_history = self.user_data.get("learning_history", [])
        self.personality_preferences = self.user_data.get("personality_preferences", {
            "default_personality": "quirky",
            "voice_name": "EVE",
            "use_tts": False
        })
    
    def _load_memory(self):
        """Load long-term memory from file."""
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default memory for Gemini
            default_memory = {
                "user_name": "Gemini",
                "created_date": datetime.now().isoformat(),
                "interests": {
                    "sound_engineering": True,
                    "competitive_gaming": True,
                    "coding": True,
                    "call_of_duty_mobile": True,
                    "audio_mixing": True,
                    "mac_optimization": True
                },
                "past_projects": [],
                "learning_history": [],
                "personality_preferences": {
                    "default_personality": "quirky",
                    "voice_name": "EVE",
                    "use_tts": False
                },
                "tags": ["sound_engineer", "gamer", "developer", "creative"]
            }
            self._save_memory(default_memory)
            return default_memory
    
    def _save_memory(self, data):
        """Save memory to file."""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    def store_project(self, project_name, description, language=None, tags=None):
        """Store a completed or in-progress project."""
        project = {
            "name": project_name,
            "description": description,
            "language": language,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat()
        }
        self.past_projects.append(project)
        self.user_data["past_projects"] = self.past_projects
        return self._save_memory(self.user_data)
    
    def store_learning(self, topic, insight, context=None):
        """Store a learned fact or pattern about the user."""
        learning = {
            "topic": topic,
            "insight": insight,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self.learning_history.append(learning)
        self.user_data["learning_history"] = self.learning_history
        return self._save_memory(self.user_data)
    
    def store_interest(self, interest_name, is_active=True):
        """Track emerging interests."""
        self.interests[interest_name] = is_active
        self.user_data["interests"] = self.interests
        return self._save_memory(self.user_data)
    
    def get_personality_context(self):
        """Get context about user for personality matching."""
        return {
            "user_name": self.user_name,
            "interests": self.interests,
            "num_projects": len(self.past_projects),
            "learning_count": len(self.learning_history),
            "tags": self.user_data.get("tags", [])
        }
    
    def build_context_prompt(self):
        """Build a context prompt to prepend to user messages."""
        context = f"""[CONTEXT ABOUT {self.user_name.upper()}]
Skills: Sound Engineer, Competitive Gamer (CoD Mobile), Full-Stack Developer
Current Interests: {', '.join([k for k, v in self.interests.items() if v])}
Recent Projects: {len(self.past_projects)} completed
Lessons Learned: {len(self.learning_history)} key insights

[RECENT LEARNINGS]"""
        
        # Add recent learnings (last 5)
        for learning in self.learning_history[-5:]:
            context += f"\n- {learning['topic']}: {learning['insight'][:80]}"
        
        return context
    
    def get_system_prompt_for_personality(self, personality="quirky"):
        """Get personality-specific system prompt with user context."""
        base_prompt = self.system_prompt
        context = self.build_context_prompt()
        return f"{base_prompt}\n\n{context}"
    
    def get_greeting(self):
        """Generate a personalized greeting based on prior context."""
        num_sessions = self.user_data.get("num_sessions", 0)
        
        greetings = {
            0: f"Hey {self.user_name}! First time? Let's create some magic together. 🎮✨",
            1: f"Welcome back, {self.user_name}! Ready to keep building? 🚀",
            2: f"{self.user_name}! Missed you. What are we shipping today? 💻",
            3: f"Back again, {self.user_name}? I've been waiting. Let's go! 🔥",
        }
        
        # Get appropriate greeting
        greeting = greetings.get(min(num_sessions, 3), 
                                f"Welcome back, {self.user_name}! What's on the agenda?")
        
        return greeting
    
    def log_session(self):
        """Log a new session."""
        self.user_data["num_sessions"] = self.user_data.get("num_sessions", 0) + 1
        self.user_data["last_session"] = datetime.now().isoformat()
        return self._save_memory(self.user_data)
    
    def add_custom_memory(self, key, value):
        """Store custom data in memory."""
        self.user_data[key] = value
        return self._save_memory(self.user_data)
    
    def get_memory_summary(self):
        """Get a summary of what the brain knows about the user."""
        return {
            "name": self.user_name,
            "sessions": self.user_data.get("num_sessions", 0),
            "projects": len(self.past_projects),
            "learnings": len(self.learning_history),
            "interests": self.interests,
            "profile_completeness": self._calculate_completeness()
        }
    
    def _calculate_completeness(self):
        """Calculate how well we know the user (0-100)."""
        completeness = 0
        
        # User name (20 points)
        if self.user_name != "Gemini":
            completeness += 20
        
        # Projects (30 points)
        if len(self.past_projects) >= 3:
            completeness += 30
        elif len(self.past_projects) >= 1:
            completeness += 15
        
        # Learnings (30 points)
        if len(self.learning_history) >= 5:
            completeness += 30
        elif len(self.learning_history) >= 1:
            completeness += 15
        
        # Interests (20 points)
        if len([i for i in self.interests.values() if i]) >= 3:
            completeness += 20
        
        return min(100, completeness)


# Convenience function for quick access
def create_brain(user_name="Gemini"):
    """Factory function to create a PersonalBrain instance."""
    brain = PersonalBrain()
    if user_name != "Gemini":
        brain.user_data["user_name"] = user_name
        brain.user_name = user_name
        brain._save_memory(brain.user_data)
    return brain


if __name__ == "__main__":
    # Demo usage
    print("PersonalBrain - EVE's Memory System")
    print("=" * 50)
    
    brain = create_brain()
    
    print(f"\n👤 Welcome to {brain.user_name}'s PersonalBrain")
    print(f"📊 Profile: {brain.get_memory_summary()}")
    print(f"\n💭 System Prompt (first 200 chars):")
    print(f"   {brain.system_prompt[:200]}...")
    print(f"\n🎮 Core Interests:")
    for interest, active in brain.interests.items():
        status = "✓" if active else "✗"
        print(f"   [{status}] {interest}")
    
    # Example: Store a project
    brain.store_project(
        "EVE AI Assistant",
        "Cyberpunk-themed AI desktop companion with voice integration",
        language="Python",
        tags=["UI", "AI", "voice"]
    )
    
    print(f"\n📚 Projects stored: {len(brain.past_projects)}")
    print(f"💡 Memory completeness: {brain.get_memory_summary()['profile_completeness']}%")
