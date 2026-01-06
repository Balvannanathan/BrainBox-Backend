from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from service.chatbot_service import process_chat_message, get_session_history


# Request/Response models
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User's message", min_length=1)
    session_id: Optional[int] = Field(None, description="Optional session ID to continue existing conversation")
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello, how are you?",
                "session_id": None,
                "user_id": "user123"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    session_id: int
    session_name: str 
    messages: list[dict]
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": 1,
                "session_name": "",
                "messages": [
                    {
                        "message_id": 1,
                        "question": "Hello, how are you?",
                        "answer": "I'm doing well, thank you! How can I help you today?"
                    }
                ],
                "timestamp": "2026-01-06T16:30:00"
            }
        }


class SessionHistoryResponse(BaseModel):
    """Response model for session history"""
    session_id: int
    session_name: str
    created_at: str
    messages: list


# Create router
router = APIRouter(prefix="/api", tags=["Chatbot"])


@router.post("/chat", response_model=ChatResponse, status_code=200)
async def chat(request: ChatRequest):
    """
    Main chatbot endpoint - Send a message and receive AI response
    
    - **message**: The user's message (required)
    - **session_id**: Optional session ID to continue existing conversation
    - **user_id**: Optional user identifier for tracking
    
    Returns the AI's response along with session information
    """
    try:
        result = process_chat_message(
            user_message=request.message,
            session_id=request.session_id,
            user_id=request.user_id
        )
        
        return ChatResponse(**result)
    
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/session/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(session_id: int):
    """
    Get complete conversation history for a session
    
    - **session_id**: The session ID to retrieve
    
    Returns session information and all messages
    """
    try:
        history = get_session_history(session_id)
        return SessionHistoryResponse(**history)
    
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )
