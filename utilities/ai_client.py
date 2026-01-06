import os
from openai import OpenAI
from typing import List, Dict
import google.generativeai as genai


# Initialize OpenAI client
_client = None

def get_ai_client():
    """Get or initialize the OpenAI client"""
    try:
        client = os.getenv("OPENAI_API_KEY")
        if not client:
            raise ValueError("OpenAI API key is not configured. Please set OPENAI_API_KEY in .env file")
        result = OpenAI(api_key=client, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        return result
    except Exception as ex:
        print(str(ex))



def generate_chat_response(user_message: str, conversation_history: List[Dict[str, str]] = None) -> str:
    """
    Generate response for a chat message with optional conversation history
    
    Args:
        user_message: The user's message
        conversation_history: Optional list of previous messages
        
    Returns:
        AI generated response
    """
    try:

        system_prompt: str = """You are a helpful AI assistant called Brainbox AI. 
            You can answer questions about normal everyday topics in a friendly and informative manner. 
            Be concise, accurate, and helpful in your responses."""

        client = get_ai_client()

        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=messages,
        )

        print(response.choices[0].message.content)
        
        return response.choices[0].message.content

    except Exception as ex:
        print(str(ex))
