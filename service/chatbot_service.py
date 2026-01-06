from typing import Optional, Dict, Any
from repository.chat_repository import create_session, get_session, get_all_sessions, update_session, delete_session, create_message, get_recent_messages, get_messages_by_session
import repository.error_log_repository as error_repo
from utilities.ai_client import generate_chat_response


def process_chat_message(
    user_message: str, 
    session_id: Optional[int] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a chat message and generate AI response
    
    Args:
        user_message: The user's message
        session_id: Optional existing session ID
        user_id: Optional user identifier
        
    Returns:
        Dictionary containing session_id, user_message, ai_response, and timestamp
    """
    try:
        # Create or get session
        if session_id:
            session = get_session(session_id)
            if not session:
                raise ValueError(f"Session with ID {session_id} not found")
        else:
            session = create_session(user_id=user_id)
            
        
        # Get conversation history for context
        conversation_history = get_conversation_history(session.id, limit=10)
        
        # Generate AI response
        ai_response = generate_chat_response(
            user_message=user_message,
            conversation_history=conversation_history
        )
        
        # Save user message
        result = create_message(
            session_id=session.id,
            answer=ai_response,
            question=user_message,
        )

        return {
            "session_id": session.id,
            "session_name": session.session_name,
                "messages": [
                    {
                        "message_id": result.id,
                        "question": result.question,
                        "answer": result.answer
                    }
                ],
        }
    
    except Exception as e:
        # Log error to database
        error_repo.log_exception(e)
        raise


def get_conversation_history(session_id: int, limit: int = 10) -> list:
    """
    Get recent conversation history for context
    
    Args:
        session_id: The session ID
        limit: Maximum number of messages to retrieve
        
    Returns:
        List of message dictionaries with role and content
    """
    messages = get_recent_messages(session_id, count=limit)
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def get_session_history(session_id: int) -> Dict[str, Any]:
    """
    Get complete session history with all messages
    
    Args:
        session_id: The session ID
        
    Returns:
        Dictionary with session info and messages
    """
    session = get_session(session_id)
    if not session:
        raise ValueError(f"Session with ID {session_id} not found")
    
    messages = get_messages_by_session(session_id)
    
    return {
        "session_id": session.id,
        "session_name": session.session_name,
        "created_at": session.created_at.isoformat(),
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    }
