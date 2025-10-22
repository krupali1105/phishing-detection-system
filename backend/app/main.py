from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict, analytics, llm_predict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Phishing Detection API",
    description="AI-powered phishing detection system using URL features and NLP analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router)
app.include_router(analytics.router)
app.include_router(llm_predict.router)

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Phishing Detection API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "predict_url": "/predict/url",
            "predict_text": "/predict/text", 
            "predict_hybrid": "/predict/hybrid",
            "llm_predict_url": "/llm-predict/url",
            "llm_predict_text": "/llm-predict/text",
            "llm_predict_hybrid": "/llm-predict/hybrid",
            "llm_status": "/llm-predict/status",
            "analytics": "/analytics/summary",
            "history": "/analytics/history"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
