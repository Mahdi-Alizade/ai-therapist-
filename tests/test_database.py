import os
import pytest
from app.services.database import (
    init_database,
    save_session,
    save_message,
    load_session_messages,
    DATABASE_FILENAME
)


@pytest.mark.asyncio
async def test_database_initialization_and_crud():
    # Ensure clean state for test
    if os.path.exists(DATABASE_FILENAME):
        try:
            os.remove(DATABASE_FILENAME)
        except OSError:
            pass

    # 1. Initialize tables
    await init_database()
    assert os.path.exists(DATABASE_FILENAME)

    test_session_id = "sess_test_101"
    test_persona = "cbt"

    # 2. Save session
    await save_session(test_session_id, test_persona)

    # 3. Save message sequence
    await save_message(test_session_id, "user", "Hello, I am testing the memory.")
    await save_message(test_session_id, "model", "I hear you clearly. How does that feel?")

    # 4. Load messages and verify order and content
    messages = await load_session_messages(test_session_id)
    assert len(messages) == 2

    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello, I am testing the memory."

    assert messages[1]["role"] == "model"
    assert messages[1]["content"] == "I hear you clearly. How does that feel?"

    # Cleanup test db artifact
    if os.path.exists(DATABASE_FILENAME):
        try:
            os.remove(DATABASE_FILENAME)
        except OSError:
            pass