import pytest
from app.core.prompts import SYSTEM_INSTRUCTION


def test_system_prompt_contains_cbt_pillars():
    prompt = SYSTEM_INSTRUCTION.lower()
    
    # Check CBT concepts
    assert "cognitive behavioral therapy" in prompt or "cbt" in prompt
    assert "socratic" in prompt
    assert "automatic thoughts" in prompt
    assert "validation" in prompt


def test_system_prompt_contains_reflective_exercises():
    prompt = SYSTEM_INSTRUCTION.lower()
    
    # Check grounding exercises
    assert "box breathing" in prompt
    assert "5-4-3-2-1" in prompt
    assert "grounding" in prompt


def test_system_prompt_enforces_safety_and_non_medical_boundaries():
    prompt = SYSTEM_INSTRUCTION.lower()
    
    # Check boundaries
    assert "not a medical doctor" in prompt or "not a licensed" in prompt
    assert "diagnoses" in prompt