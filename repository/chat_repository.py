from sqlalchemy.orm import Session
from models import ChatSession, ChatMessage
from typing import Optional, List
from datetime import datetime
from utilities.database import get_db


def create_session(user_id: Optional[str] = None, session_name: Optional[str] = None) -> ChatSession:
    """Create a new chat session"""
    db = next(get_db())
    try:
        session = ChatSession(
            user_id=user_id,
            session_name=session_name or f"Chat Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )
        db.add(session)
        db.commit()
        db.refresh(session)

        return session
    finally:
        db.close()


def get_session(session_id: int) -> Optional[ChatSession]:
    """Get a chat session by ID"""
    db = next(get_db())
    try:
        return db.query(ChatSession).filter(ChatSession.id == session_id).first()
    finally:
        db.close()


def get_all_sessions(user_id: Optional[str] = None) -> List[ChatSession]:
    """Get all chat sessions, optionally filtered by user_id"""
    db = next(get_db())
    try:
        query = db.query(ChatSession)
        if user_id:
            query = query.filter(ChatSession.user_id == user_id)
        return query.order_by(ChatSession.created_at.desc()).all()
    finally:
        db.close()


def update_session(session_id: int, session_name: Optional[str] = None) -> Optional[ChatSession]:
    """Update a chat session"""
    db = next(get_db())
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            if session_name:
                session.session_name = session_name
            session.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(session)
        return session
    finally:
        db.close()


def delete_session(session_id: int) -> bool:
    """Delete a chat session"""
    db = next(get_db())
    try:
        session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if session:
            db.delete(session)
            db.commit()
            return True
        return False
    finally:
        db.close()


def create_message(session_id: int, question: str, answer: str) -> ChatMessage:
    """Create a new chat message"""
    db = next(get_db())
    try:
        message = ChatMessage(
            session_id=session_id,
            question=question,
            answer=answer
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    finally:
        db.close()


def get_message(message_id: int) -> Optional[ChatMessage]:
    """Get a specific message by ID"""
    db = next(get_db())
    try:
        return db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    finally:
        db.close()


def get_messages_by_session(session_id: int, limit: Optional[int] = None) -> List[ChatMessage]:
    """Get all messages for a specific session"""
    db = next(get_db())
    try:
        query = db.query(ChatMessage).filter(ChatMessage.session_id == session_id)
        query = query.order_by(ChatMessage.timestamp.asc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    finally:
        db.close()


def get_recent_messages(session_id: int, count: int = 10) -> List[ChatMessage]:
    """Get the most recent N messages for a session"""
    db = next(get_db())
    try:
        return db.query(ChatMessage)\
            .filter(ChatMessage.session_id == session_id)\
            .order_by(ChatMessage.timestamp.desc())\
            .limit(count)\
            .all()[::-1]  # Reverse to get chronological order
    finally:
        db.close()
