import pytest
from app.core.prompts import (
    PERSONA_PROMPTS,
    DEFAULT_PERSONA,
    get_system_instruction,
)


def test_persona_keys_exist():
    expected_personas = {"cbt", "stoic", "rubber_duck"}
    assert set(PERSONA_PROMPTS.keys()) == expected_personas


def test_cbt_prompt_content():
    prompt = get_system_instruction("cbt").lower()
    assert "cognitive behavioral therapy" in prompt or "cbt" in prompt
    assert "socratic" in prompt
    assert "box breathing" in prompt


def test_stoic_prompt_content():
    prompt = get_system_instruction("stoic").lower()
    assert "dichotomy of control" in prompt
    assert "marcus aurelius" in prompt or "stoic" in prompt


def test_rubber_duck_prompt_content():
    prompt = get_system_instruction("rubber_duck").lower()
    assert "rubber duck" in prompt
    assert "stack trace" in prompt or "burnout" in prompt


def test_fallback_to_default_on_unknown_persona():
    fallback_prompt = get_system_instruction("unknown_style")
    default_prompt = get_system_instruction(DEFAULT_PERSONA)
    assert fallback_prompt == default_prompt