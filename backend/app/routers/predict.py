from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from app.utils.load_models import predict_url, predict_text, predict_hybrid
from app.db import get_db, PredictionLog
from datetime import datetime
import logging

router = APIRouter(prefix="/predict", tags=["Prediction"])
logger = logging.getLogger(__name__)

class URLRequest(BaseModel):
    url: str
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com"
            }
        }

class TextRequest(BaseModel):
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Please verify your account immediately to avoid suspension."
            }
        }

class HybridRequest(BaseModel):
    url: str
    text: str = None
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com",
                "text": "Please verify your account immediately to avoid suspension."
            }
        }

class PredictionResponse(BaseModel):
    url: str = None
    text: str = None
    prediction: str
    confidence: float
    model_type: str
    timestamp: datetime

def log_prediction(db: Session, url: str = None, text: str = None, 
                  prediction: str = None, confidence: float = None, 
                  model_type: str = None, request: Request = None):
    """Log prediction to database."""
    try:
        log_entry = PredictionLog(
            url=url,
            text=text,
            prediction=prediction,
            confidence=confidence,
            model_type=model_type,
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Error logging prediction: {e}")
        db.rollback()

@router.post("/url", response_model=PredictionResponse)
def predict_url_endpoint(request: URLRequest, db: Session = Depends(get_db), http_request: Request = None):
    """Predict phishing probability for a URL."""
    try:
        logger.info(f"Predict URL requested: url={request.url}")
        result, confidence = predict_url(request.url)
        logger.info(f"Predict URL result: url={request.url} result={result} confidence={confidence:.4f}")
        
        # Log prediction
        log_prediction(db, url=request.url, prediction=result, 
                      confidence=confidence, model_type="url", request=http_request)
        
        return PredictionResponse(
            url=request.url,
            prediction=result,
            confidence=confidence,
            model_type="url",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error in URL prediction for url={request.url}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/text", response_model=PredictionResponse)
def predict_text_endpoint(request: TextRequest, db: Session = Depends(get_db), http_request: Request = None):
    """Predict phishing probability for text content."""
    try:
        logger.info("Predict Text requested")
        result, confidence = predict_text(request.text)
        logger.info(f"Predict Text result: result={result} confidence={confidence:.4f}")
        
        # Log prediction
        log_prediction(db, text=request.text, prediction=result, 
                      confidence=confidence, model_type="text", request=http_request)
        
        return PredictionResponse(
            text=request.text,
            prediction=result,
            confidence=confidence,
            model_type="text",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error in text prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/hybrid", response_model=PredictionResponse)
def predict_hybrid_endpoint(request: HybridRequest, db: Session = Depends(get_db), http_request: Request = None):
    """Predict phishing probability using hybrid model (URL + text)."""
    try:
        logger.info(f"Predict Hybrid requested: url={request.url} text_present={bool(request.text)}")
        result, confidence = predict_hybrid(request.url, request.text)
        logger.info(f"Predict Hybrid result: url={request.url} result={result} confidence={confidence:.4f}")
        
        # Log prediction
        log_prediction(db, url=request.url, text=request.text, prediction=result, 
                      confidence=confidence, model_type="hybrid", request=http_request)
        
        return PredictionResponse(
            url=request.url,
            text=request.text,
            prediction=result,
            confidence=confidence,
            model_type="hybrid",
            timestamp=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"Error in hybrid prediction for url={request.url}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
