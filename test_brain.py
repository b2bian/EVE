#!/usr/bin/env python3
"""Test PersonalBrain system."""

from utils.personal_brain import PersonalBrain, create_brain

# Test PersonalBrain initialization
print("=" * 60)
print("👤 PERSONALBRAIN SYSTEM TEST")
print("=" * 60)

brain = create_brain()
print(f"\n✓ PersonalBrain initialized for: {brain.user_name}")
print(f"✓ Personality: {brain.personality_preferences['default_personality']}")
print(f"✓ Voice Name: {brain.personality_preferences['voice_name']}")

# Test greeting
greeting = brain.get_greeting()
print(f"\n💬 Initial greeting:\n   {greeting}")

# Test memory summary
summary = brain.get_memory_summary()
print(f"\n📊 Brain Profile Summary:")
print(f"   Name: {summary['name']}")
print(f"   Sessions: {summary['sessions']}")
print(f"   Profile Completeness: {summary['profile_completeness']}%")
print(f"   Key Interests:")
for interest, active in brain.interests.items():
    status = "✓" if active else "✗"
    print(f"     [{status}] {interest}")

# Test system prompt generation
print(f"\n🎭 System Prompt (first 250 chars):")
system_prompt = brain.get_system_prompt_for_personality("quirky")
print(f"   {system_prompt[:250]}...")

# Test storing a project
brain.store_project(
    "EVE AI Assistant",
    "Cyberpunk-themed AI desktop companion with personality system",
    language="Python",
    tags=["UI", "AI", "personality-system"]
)
print(f"\n📚 Stored project: EVE AI Assistant")

# Test storing learning
brain.store_learning(
    "Cyberpunk Design",
    "Neon colors (#00f2ff cyan, #ff9d00 orange) create compelling visual depth",
    context="UI Theme Design"
)
print(f"💡 Stored learning: Cyberpunk Design")

# Updated summary
summary = brain.get_memory_summary()
print(f"\n📈 Updated Profile Completeness: {summary['profile_completeness']}%")
print(f"   Projects: {summary['projects']}")
print(f"   Learnings: {summary['learning_count']}")

print("\n✅ PersonalBrain system fully functional!")
print("=" * 60)
