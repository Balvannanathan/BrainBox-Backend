from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class ChatSession(Base):
    """Model for storing chat session information"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), nullable=True)
    session_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with messages
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")



class ChatMessage(Base):
    """Model for storing individual chat messages"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with session
    session = relationship("ChatSession", back_populates="messages")


class ErrorLog(Base):
    """Model for storing application errors"""
    __tablename__ = "error_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    error_type = Column(String(100), nullable=False)
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    


class Prompt(Base):
    """Model for storing prompt templates and history"""
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prompt_text = Column(Text, nullable=False)
    prompt_type = Column(String(100), nullable=True)  # e.g., 'system', 'template', 'user'
    created_at = Column(DateTime, default=datetime.utcnow)
    
