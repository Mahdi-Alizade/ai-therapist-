import os
import pytest
from datetime import datetime, timezone, timedelta
from app.services.database import (
    init_database,
    save_session,
    save_message,
    load_session_messages,
    cleanup_expired_sessions,
    get_connection,
    DATABASE_FILENAME
)


@pytest.mark.asyncio
async def test_database_initialization_and_crud():
    if os.path.exists(DATABASE_FILENAME):
        try:
            os.remove(DATABASE_FILENAME)
        except OSError:
            pass

    await init_database()
    assert os.path.exists(DATABASE_FILENAME)

    test_session_id = "sess_test_101"
    test_persona = "cbt"

    await save_session(test_session_id, test_persona)

    await save_message(test_session_id, "user", "Hello, I am testing the memory.")
    await save_message(test_session_id, "model", "I hear you clearly. How does that feel?")

    messages = await load_session_messages(test_session_id)
    assert len(messages) == 2

    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello, I am testing the memory."

    assert messages[1]["role"] == "model"
    assert messages[1]["content"] == "I hear you clearly. How does that feel?"

    if os.path.exists(DATABASE_FILENAME):
        try:
            os.remove(DATABASE_FILENAME)
        except OSError:
            pass


@pytest.mark.asyncio
async def test_cleanup_expired_sessions_logic():
    await init_database()
    conn = await get_connection()

    old_session_id = "sess_old_retention_999"
    active_session_id = "sess_active_retention_111"

    # Insert an old session older than 40 days
    past_date = datetime.now(timezone.utc) - timedelta(days=45)
    past_str = past_date.isoformat()

    try:
        await conn.execute(
            "INSERT INTO chat_sessions (session_id, persona, created_at) VALUES (?, ?, ?);",
            (old_session_id, "cbt", past_str)
        )
        await conn.execute(
            "INSERT INTO chat_messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?);",
            (old_session_id, "user", "Old message to purge", past_str)
        )
        await conn.commit()
    finally:
        await conn.close()

    # Insert an active session via standard method
    await save_session(active_session_id, "cbt")
    await save_message(active_session_id, "user", "Recent message to keep")

    # Run cleanup with default 30-day retention
    purged_count = await cleanup_expired_sessions(retention_days=30)
    assert purged_count >= 1

    # Verify old session was removed
    old_messages = await load_session_messages(old_session_id)
    assert len(old_messages) == 0

    # Verify active session remains intact
    active_messages = await load_session_messages(active_session_id)
    assert len(active_messages) == 1
    assert active_messages[0]["content"] == "Recent message to keep"