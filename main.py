from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from controller.chatbot_controller import router as chatbot_router
from utilities.database import init_db
import uvicorn


# Create FastAPI application
app = FastAPI(
    description="AI Chatbot API with conversation management"
)

# Register routers
app.include_router(chatbot_router)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "healthy",
        "message": "Welcome to Brainbox AI! Visit /docs for API documentation."
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":

    uvicorn.run(
        host="0.0.0.0",
        port=8000,
        reload=True
    )
