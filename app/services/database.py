import os
import aiosqlite
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_FILENAME = "therapist_sessions.db"


async def get_connection() -> aiosqlite.Connection:
    conn = await aiosqlite.connect(DATABASE_FILENAME)
    conn.row_factory = aiosqlite.Row
    return conn


async def init_database() -> None:
    conn = await get_connection()
    try:
        # Create sessions table
        create_sessions_query = """
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            persona TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
        await conn.execute(create_sessions_query)

        # Create messages table
        create_messages_query = """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
        );
        """
        await conn.execute(create_messages_query)
        await conn.commit()
    finally:
        await conn.close()


async def save_session(session_id: str, persona: str) -> None:
    conn = await get_connection()
    try:
        now_str = datetime.utcnow().isoformat()
        insert_query = """
        INSERT OR IGNORE INTO chat_sessions (session_id, persona, created_at)
        VALUES (?, ?, ?);
        """
        await conn.execute(insert_query, (session_id, persona, now_str))
        await conn.commit()
    finally:
        await conn.close()


async def save_message(session_id: str, role: str, content: str) -> None:
    conn = await get_connection()
    try:
        timestamp_now = datetime.utcnow().isoformat()
        insert_msg_query = """
        INSERT INTO chat_messages (session_id, role, content, created_at)
        VALUES (?, ?, ?, ?);
        """
        await conn.execute(insert_msg_query, (session_id, role, content, timestamp_now))
        await conn.commit()
    finally:
        await conn.close()


async def load_session_messages(session_id: str) -> List[Dict[str, str]]:
    conn = await get_connection()
    results: List[Dict[str, str]] = []
    try:
        select_query = """
        SELECT role, content
        FROM chat_messages
        WHERE session_id = ?
        ORDER BY id ASC;
        """
        async with conn.execute(select_query, (session_id,)) as cursor:
            rows = await cursor.fetchall()
            for r in rows:
                message_item = {
                    "role": r["role"],
                    "content": r["content"]
                }
                results.append(message_item)
    finally:
        await conn.close()

    return results