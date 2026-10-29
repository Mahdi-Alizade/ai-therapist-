import os
import aiosqlite
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

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

        # Create structured CBT thought records table
        create_thought_records_query = """
        CREATE TABLE IF NOT EXISTS thought_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            situation TEXT NOT NULL,
            automatic_thought TEXT NOT NULL,
            distortion TEXT NOT NULL,
            rational_reframe TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
        );
        """
        await conn.execute(create_thought_records_query)
        await conn.commit()
    finally:
        await conn.close()


async def save_session(session_id: str, persona: str) -> None:
    conn = await get_connection()
    try:
        now_str = datetime.now(timezone.utc).isoformat()
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
        timestamp_now = datetime.now(timezone.utc).isoformat()
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


async def save_thought_record(
    session_id: str,
    situation: str,
    automatic_thought: str,
    distortion: str,
    rational_reframe: str
) -> int:
    conn = await get_connection()
    try:
        timestamp_now = datetime.now(timezone.utc).isoformat()
        insert_query = """
        INSERT INTO thought_records (session_id, situation, automatic_thought, distortion, rational_reframe, created_at)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor = await conn.execute(
            insert_query,
            (session_id, situation, automatic_thought, distortion, rational_reframe, timestamp_now)
        )
        await conn.commit()
        return cursor.lastrowid or 0
    finally:
        await conn.close()


async def load_thought_records(session_id: str) -> List[Dict[str, Any]]:
    conn = await get_connection()
    records: List[Dict[str, Any]] = []
    try:
        select_query = """
        SELECT id, situation, automatic_thought, distortion, rational_reframe, created_at
        FROM thought_records
        WHERE session_id = ?
        ORDER BY id DESC;
        """
        async with conn.execute(select_query, (session_id,)) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                records.append({
                    "id": row["id"],
                    "situation": row["situation"],
                    "automatic_thought": row["automatic_thought"],
                    "distortion": row["distortion"],
                    "rational_reframe": row["rational_reframe"],
                    "created_at": row["created_at"]
                })
    finally:
        await conn.close()
    return records