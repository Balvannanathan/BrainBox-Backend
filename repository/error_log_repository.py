from sqlalchemy.orm import Session
from models import ErrorLog
from typing import List, Optional
import traceback
from utilities.database import get_db


def log_error(error_type: str, error_message: str, stack_trace: Optional[str] = None) -> ErrorLog:
    """Create a new error log entry"""
    db = next(get_db())
    try:
        error_log = ErrorLog(
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace
        )
        db.add(error_log)
        db.commit()
        db.refresh(error_log)
        return error_log
    finally:
        db.close()


def log_exception(exception: Exception) -> ErrorLog:
    """Log an exception with full stack trace"""
    return log_error(
        error_type=type(exception).__name__,
        error_message=str(exception),
        stack_trace=traceback.format_exc()
    )


def get_recent_errors(limit: int = 50) -> List[ErrorLog]:
    """Get recent error logs"""
    db = next(get_db())
    try:
        return db.query(ErrorLog)\
            .order_by(ErrorLog.timestamp.desc())\
            .limit(limit)\
            .all()
    finally:
        db.close()


def get_errors_by_type(error_type: str, limit: int = 50) -> List[ErrorLog]:
    """Get error logs filtered by error type"""
    db = next(get_db())
    try:
        return db.query(ErrorLog)\
            .filter(ErrorLog.error_type == error_type)\
            .order_by(ErrorLog.timestamp.desc())\
            .limit(limit)\
            .all()
    finally:
        db.close()
