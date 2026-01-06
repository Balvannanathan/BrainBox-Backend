from sqlalchemy.orm import Session
from models import Prompt
from typing import List, Optional
from utilities.database import get_db


def create_prompt(prompt_text: str, prompt_type: Optional[str] = None) -> Prompt:
    """Create a new prompt entry"""
    db = next(get_db())
    try:
        prompt = Prompt(
            prompt_text=prompt_text,
            prompt_type=prompt_type
        )
        db.add(prompt)
        db.commit()
        db.refresh(prompt)
        return prompt
    finally:
        db.close()


def get_prompt(prompt_id: int) -> Optional[Prompt]:
    """Get a specific prompt by ID"""
    db = next(get_db())
    try:
        return db.query(Prompt).filter(Prompt.id == prompt_id).first()
    finally:
        db.close()


def get_all_prompts(prompt_type: Optional[str] = None) -> List[Prompt]:
    """Get all prompts, optionally filtered by type"""
    db = next(get_db())
    try:
        query = db.query(Prompt)
        if prompt_type:
            query = query.filter(Prompt.prompt_type == prompt_type)
        return query.order_by(Prompt.created_at.desc()).all()
    finally:
        db.close()


def get_recent_prompts(limit: int = 10) -> List[Prompt]:
    """Get recent prompts"""
    db = next(get_db())
    try:
        return db.query(Prompt)\
            .order_by(Prompt.created_at.desc())\
            .limit(limit)\
            .all()
    finally:
        db.close()
