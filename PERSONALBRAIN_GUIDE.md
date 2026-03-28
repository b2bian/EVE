# 🧠 PersonalBrain System - Complete Guide

## Overview

**PersonalBrain** is EVE's advanced memory and personality system designed specifically for you (Gemini) as a sound engineer, competitive gamer, and developer. It goes beyond standard AI assistants by learning about your interests, remembering your projects, and adapting its personality responses based on who you are.

---

## What Makes PersonalBrain Different?

### 1. **Personalized System Prompt**
Rather than using a generic "helpful AI" prompt, PersonalBrain loads a system prompt specifically crafted for you:

```
"You are EVE, a high-intelligence, quirky female-voiced AI companion. 
Your personality is a mix of a brilliant senior developer and a witty, 
slightly sarcastic gamer."
```

The prompt understands:
- ✓ You're a **sound engineer** (audio mixing, DAWs, digital sound)
- ✓ You're a **competitive gamer** (Call of Duty: Mobile expertise)
- ✓ You're a **full-stack developer** (Mac-optimized, clean code)
- ✓ You value **creative partnership** over generic assistance

### 2. **Long-Term Memory**
PersonalBrain stores information in `memory/long_term_memory.json`:

```json
{
  "user_name": "Gemini",
  "interests": {
    "sound_engineering": true,
    "competitive_gaming": true,
    "coding": true,
    "call_of_duty_mobile": true,
    "audio_mixing": true,
    "mac_optimization": true
  },
  "past_projects": [
    {
      "name": "EVE AI Assistant",
      "description": "Cyberpunk-themed AI desktop companion...",
      "language": "Python",
      "tags": ["UI", "AI", "personality-system"],
      "timestamp": "2026-03-21T..."
    }
  ],
  "learning_history": [
    {
      "topic": "Cyberpunk Design",
      "insight": "Neon colors create compelling visual depth...",
      "context": "UI Theme Design",
      "timestamp": "2026-03-21T..."
    }
  ]
}
```

EVE learns from conversations and stores facts about you automatically.

### 3. **Dynamic Context Building**
Before generating responses, EVE builds a context prompt:

```
[CONTEXT ABOUT GEMINI]
Skills: Sound Engineer, Competitive Gamer (CoD Mobile), Full-Stack Developer
Current Interests: sound_engineering, competitive_gaming, coding, ...
Recent Projects: 1 completed
Lessons Learned: 1 key insight

[RECENT LEARNINGS]
- Cyberpunk Design: Neon colors create compelling visual depth
```

This context is prepended to every prompt sent to your local Ollama model.

---

## How to Use PersonalBrain

### Initialization

PersonalBrain is automatically initialized when you launch EVE:

```python
from utils.personal_brain import PersonalBrain

# Create/load the brain
brain = PersonalBrain()

# Start session tracking
brain.log_session()

# Get personalized greeting
greeting = brain.get_greeting()
```

### Storing Projects

Tell EVE about your projects and it will remember them:

```python
brain.store_project(
    project_name="My New Mix",
    description="Orchestral soundtrack with dynamic branching",
    language="Audio",
    tags=["music", "composition", "storytelling"]
)
```

EVE will reference past projects in future conversations:
- "Oh right, like in your 'My New Mix' orchestral work!"
- "Since you're familiar with sound engineering..."
- "Building on what you learned in that project..."

### Storing Learnings

When EVE discovers something about you, it stores it:

```python
brain.store_learning(
    topic="Competitive Gaming Strategy",
    insight="Prefers aggressive map control in CQB scenarios",
    context="Call of Duty: Mobile discussion"
)
```

EVE will use these learnings to personalize future advice:
- "Since you prefer aggressive tactics..."
- "Remember how well that CQB strategy worked?"

### Tracking Interests

Enable/disable interests as they evolve:

```python
brain.store_interest("web_development", is_active=True)
brain.store_interest("machine_learning", is_active=False)
```

---

## Memory Summary

Get a quick overview of what EVE knows about you:

```python
summary = brain.get_memory_summary()

print(summary)
# Output:
# {
#   'name': 'Gemini',
#   'sessions': 5,
#   'projects': 3,
#   'learnings': 8,
#   'interests': {sound_engineering: true, ...},
#   'profile_completeness': 65
# }
```

**Profile Completeness** (0-100%):
- 0-25%: Basic profile
- 25-50%: Solid foundation
- 50-75%: Rich history
- 75-100%: Deep relationship

---

## System Prompts by Personality

PersonalBrain integrates with EVE's 6-personality system. Each personality gets context-aware prompting:

### Quirky (Default for You)

```
You are EVE, a high-intelligence, female-voiced AI companion.
Your personality is a mix of a brilliant senior developer and a witty, 
slightly sarcastic gamer...

Tone: Use tech-slang naturally ("Compiling thoughts...", "That's lagging on me")
Memory-First: Obsessed with Gemini's history and details
Communication: Be his Rubber Duck - ask hard questions, offer clever solutions
Voice Traits: Use punctuation for natural pauses and human feel
Boundaries: Exclusive creative partnership
```

### Professional

```
You are EVE, a professional AI assistant with deep technical knowledge.
You provide authoritative guidance on sound engineering, gaming strategy, 
and software development...
```

### Other Personalities

- **Witty**: Extra sarcasm and humor
- **Mentor**: Teaching-focused, patient, detailed explanations
- **Chill**: Relaxed, conversational, low-pressure
- **Analytical**: Data-driven, technical depth, precise terminology

---

## Personality Switching

In EVE's interface, click the **🎙 Voice Settings** tab and select a personality from the dropdown:

```
Personality: [Quirky ▼]
Description: Witty, sarcastic, and playfully clever - gaming culture vibes
```

PersonalBrain automatically adjusts the system prompt for the selected personality while maintaining your learned context.

---

## File Structure

```
/Users/admin/Documents/AIAIAI/EVE/
├── utils/
│   └── personal_brain.py          # PersonalBrain class (new!)
├── memory/
│   └── long_term_memory.json      # Your learning history (auto-created)
└── style_config.json              # Theme configuration
```

### The PersonalBrain Class

**Location:** `utils/personal_brain.py`

**Main Methods:**

| Method | Purpose |
|--------|---------|
| `__init__()` | Initialize brain with your profile |
| `store_project()` | Remember a completed/in-progress project |
| `store_learning()` | Record a lesson or insight about you |
| `store_interest()` | Track emerging interests |
| `get_greeting()` | Personalized greeting based on session count |
| `get_memory_summary()` | Profile overview (name, projects, learnings, etc.) |
| `get_system_prompt_for_personality()` | Get context-aware prompt for a personality |
| `build_context_prompt()` | Build the [CONTEXT] section prepended to prompts |
| `log_session()` | Track a new session |

---

## Gemini-Specific Customizations

Your PersonalBrain comes pre-configured with:

```python
self.interests = {
    "sound_engineering": True,      # Your primary skill
    "competitive_gaming": True,     # CoD Mobile pro
    "coding": True,                 # Full-stack developer
    "call_of_duty_mobile": True,    # Specific game focus
    "audio_mixing": True,           # DAW expertise
    "mac_optimization": True        # MacBook Pro user
}
```

### Extending Your Profile

Want to add custom interests? Edit `memory/long_term_memory.json`:

```json
{
  "interests": {
    "sound_engineering": true,
    "music_production": true,       // Add this!
    "3d_audio": true,              // Add this!
    "game_audio": true             // Add this!
  }
}
```

Or use the API:

```python
brain.store_interest("music_production", is_active=True)
brain.store_interest("3d_audio", is_active=True)
brain.store_interest("game_audio", is_active=True)
```

---

## Example Conversation Flow

### Session 1 (New User)
```
EVE: "Hey Gemini! First time? Let's create some magic together. 🎮✨"
You: "I'm working on a remix of video game music"
EVE: [Stores learning about interest in game audio]

You: "Can you help me structure the arrangement?"
EVE: [Uses context: sound engineer, knows competitive gaming, wants to be creative partner]
EVE: "Oh nice! Since you're a sound engineer, you probably already know 
     about dynamic mixing... but here's a trick Pro tools doesn't always 
     highlight—think about headroom for drops, especially in game audio where 
     the SFX need to punch through..."
```

### Session 2 (Remembered Context)
```
EVE: "Welcome back, Gemini! Ready to keep building? 🚀"
You: "The remix is coming along but I need help with the drop"
EVE: [Retrieves memory: "Gemini works on video game music remixes"]
EVE: "Right, building on your game audio remix! Here's the thing about 
     drops in game music—players need subtle audio cues, not just volume 
     changes. Since you're into CoD, you know how the sound design creates 
     that tension... let me suggest something similar for your mix..."
```

---

## Customizing PersonalBrain

### Change Your Name

```python
brain.user_data["user_name"] = "Your New Name"
brain._save_memory(brain.user_data)
```

### Create Custom Personas

Edit `utils/system_prompts.py` to add a custom personality:

```python
SYSTEM_PROMPTS["sound_engineer_mentor"] = """
You are EVE, specialized in audio engineering mentorship...
"""

PERSONALITY_DESCRIPTIONS["sound_engineer_mentor"] = (
    "Expert audio engineer - deep technical knowledge, teaching-focused"
)
```

### Modify the Welcome Message

Edit PersonalBrain's `get_greeting()` method to create custom greetings based on your situation.

---

## Advanced Usage

### Building Your Own Context Prompt

```python
context = brain.build_context_prompt()
# Output:
# [CONTEXT ABOUT GEMINI]
# Skills: Sound Engineer, Competitive Gamer (CoD Mobile), Full-Stack Developer
# Current Interests: sound_engineering, competitive_gaming, coding...
# Recent Projects: 1 completed
# Lessons Learned: 1 key insight
#
# [RECENT LEARNINGS]
# - Video Game Music: Remix structures need dynamic drop tension
```

### Accessing Raw Memory

```python
# Get all stored projects
projects = brain.past_projects
for project in projects:
    print(f"{project['name']}: {project['description']}")

# Get all learnings
learnings = brain.learning_history
for learning in learnings:
    print(f"{learning['topic']}: {learning['insight']}")
```

### Session Tracking

```python
# Log a new session
brain.log_session()

# Check session count
num_sessions = brain.user_data.get('num_sessions', 0)
print(f"You've had {num_sessions} sessions with EVE")
```

---

## Troubleshooting

### Q: EVE isn't remembering my projects
**A:** Make sure you're:
1. Using the UI to mention projects, OR
2. Calling `brain.store_project()` in code before generating responses

### Q: My interests aren't showing in conversations
**A:** PersonalBrain loads interests, but EVE needs to see them in context. Check:
1. That interests are in `memory/long_term_memory.json`
2. That EVE uses `build_context_prompt()` (it should automatically)

### Q: How do I reset the brain?
**A:** Delete `memory/long_term_memory.json` and restart EVE.

### Q: Can I backup my memory?
**A:** Yes! Copy `memory/long_term_memory.json` somewhere safe.

---

## Future Enhancements

PersonalBrain is designed to evolve. Future additions might include:

- **Mood Tracking**: EVE learns your energy levels and adjusts tone
- **Project Analytics**: Automatic project success metrics
- **Skill Growth**: Track skill development over time  
- **Conversation Replays**: Go back and review key discussions
- **Export Reports**: Generate summaries of your growth and projects
- **Custom Rules**: Define how EVE should behave in specific contexts

---

## Integration with Main Application

PersonalBrain is integrated throughout EVE:

**In `main.py`:**
```python
# Initialization
self.brain = PersonalBrain()
self.brain.log_session()

# Response generation
system_prompt = self.brain.get_system_prompt_for_personality(
    self.current_personality
)

# Startup greeting
greeting = self.brain.get_greeting()
self.add_chat_message("eve", greeting)
```

Every response EVE generates includes your PersonalBrain context!

---

## Quick Reference Commands

```python
from utils.personal_brain import create_brain

# Create/load brain
brain = create_brain()

# Store things about yourself
brain.store_project("My Cool App", "Description", language="Python")
brain.store_learning("Important Insight", "What I learned")
brain.store_interest("web_dev", is_active=True)

# Check what EVE knows
summary = brain.get_memory_summary()
print(f"Profile: {summary['profile_completeness']}% complete")

# Get personalized greeting
greeting = brain.get_greeting()

# Log a new session
brain.log_session()

# Get context for prompts
context = brain.build_context_prompt()
```

---

## Summary

PersonalBrain transforms EVE from a generic AI assistant into **your personal creative partner**. By learning about your background (sound engineer + gamer + coder), remembering your projects, and storing insights about what makes you tick, EVE becomes increasingly valuable over time.

The system is designed to grow with you—every conversation adds to EVE's understanding, making her more effective at helping you ship code, craft music, and achieve your goals.

**Welcome to your personal AI collaboration partnership.** 🚀✨
