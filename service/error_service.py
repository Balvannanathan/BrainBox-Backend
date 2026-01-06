from typing import Optional
import repository.error_log_repository as error_repo


def log_application_error(
    error_type: str, 
    error_message: str, 
    stack_trace: Optional[str] = None
) -> int:
    """
    Log an application error
    
    Args:
        error_type: Type/category of the error
        error_message: Error message
        stack_trace: Optional stack trace
        
    Returns:
        ID of the created error log entry
    """
    error_log = error_repo.log_error(
        error_type=error_type,
        error_message=error_message,
        stack_trace=stack_trace
    )
    return error_log.id


def log_exception(exception: Exception) -> int:
    """
    Log an exception with full stack trace
    
    Args:
        exception: The exception to log
        
    Returns:
        ID of the created error log entry
    """
    error_log = error_repo.log_exception(exception)
    return error_log.id
