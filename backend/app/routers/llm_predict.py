"""
LLM-based prediction endpoints for enhanced phishing analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db, PredictionLog
from app.utils.llm_analyzer import llm_analyzer, LLMAnalysisResult
from datetime import datetime
import logging
from langchain.prompts import PromptTemplate  # type: ignore
from langchain.chains import LLMChain  # type: ignore
from app.utils.llm_analyzer import final_url_analysis  # add this import


router = APIRouter(prefix="/llm-predict", tags=["LLM Prediction"])
logger = logging.getLogger(__name__)

class URLRequest(BaseModel):
    url: str
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://secure-bank-verification.tk/login"
            }
        }

class TextRequest(BaseModel):
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "text": "URGENT: Your account has been suspended. Click here immediately to verify your identity."
            }
        }

class HybridRequest(BaseModel):
    url: str
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://secure-bank-verification.tk/login",
                "text": "URGENT: Your account has been suspended. Click here immediately to verify your identity."
            }
        }

class LLMPredictionResponse(BaseModel):
    url: str = None
    text: str = None
    prediction: str
    confidence: float
    explanation: str
    risk_factors: list
    recommendations: list
    model_type: str
    timestamp: datetime
    llm_model: str

def log_llm_prediction(db: Session, url: str = None, text: str = None, 
                      result: LLMAnalysisResult = None, model_type: str = None, 
                      request: Request = None):
    """Log LLM prediction to database."""
    try:
        log_entry = PredictionLog(
            url=url,
            text=text,
            prediction=result.prediction,
            confidence=result.confidence,
            model_type=f"llm_{model_type}",
            ip_address=request.client.host if request else None,
            user_agent=request.headers.get("user-agent") if request else None
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Error logging LLM prediction: {e}")
        db.rollback()

@router.get("/status")
def get_llm_status():
    """Check LLM service status and available models."""
    try:
        is_available = llm_analyzer.is_available()
        available_models = llm_analyzer.get_available_models()
        
        return {
            "available": is_available,
            "current_model": llm_analyzer.model_name,
            "available_models": available_models,
            "base_url": llm_analyzer.base_url
        }
    except Exception as e:
        logger.error(f"Error checking LLM status: {e}")
        raise HTTPException(status_code=500, detail="Failed to check LLM status")

@router.post("/url", response_model=LLMPredictionResponse)
def predict_url_llm(request: URLRequest, db: Session = Depends(get_db), http_request: Request = None):
    """Analyze URL using LLM for enhanced phishing detection."""
    try:
        logger.info(f"LLM URL prediction requested: url={request.url}")
        
        # Try to use LLM if available, otherwise fallback to ML only
        if llm_analyzer.is_available():
            prediction, confidence = final_url_analysis(request.url)
            explanation = f"Hybrid ML+LLM analysis (ML + {llm_analyzer.model_name})"
        else:
            # Fallback to ML-only analysis
            from app.utils.load_models import model_loader
            ml_result, ml_confidence = model_loader.predict_url(request.url)
            prediction = ml_result.upper()
            confidence = ml_confidence
            explanation = "ML-only analysis (LLM unavailable)"

        result = LLMAnalysisResult(
            prediction=prediction,
            confidence=confidence,
            explanation=explanation,
            risk_factors=[],
            recommendations=[]
        )
        
        # Log prediction
        log_llm_prediction(db, url=request.url, result=result, 
                          model_type="url", request=http_request)
        
        logger.info(f"LLM URL prediction result: url={request.url} prediction={prediction} confidence={confidence:.4f}")
        
        return LLMPredictionResponse(
            url=request.url,
            prediction=result.prediction,
            confidence=result.confidence,
            explanation=result.explanation,
            risk_factors=result.risk_factors,
            recommendations=result.recommendations,
            model_type="url",
            timestamp=datetime.utcnow(),
            llm_model=llm_analyzer.model_name if llm_analyzer.is_available() else "ml-only"
        )
    except Exception as e:
        logger.error(f"Error in LLM URL prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/text", response_model=LLMPredictionResponse)
def predict_text_llm(request: TextRequest, db: Session = Depends(get_db), http_request: Request = None):
    """Analyze text using LLM for enhanced phishing detection."""
    try:
        logger.info(f"LLM text prediction requested: text_length={len(request.text)}")
        
        # Try to use LLM if available, otherwise fallback to ML only
        if llm_analyzer.is_available():
            result = llm_analyzer.analyze_text(request.text)
        else:
            # Fallback to ML-only analysis
            from app.utils.load_models import model_loader
            ml_result, ml_confidence = model_loader.predict_text(request.text)
            result = LLMAnalysisResult(
                prediction=ml_result.upper(),
                confidence=ml_confidence,
                explanation="ML-only analysis (LLM unavailable)",
                risk_factors=[],
                recommendations=[]
            )
        
        # Log prediction
        log_llm_prediction(db, text=request.text, result=result, 
                          model_type="text", request=http_request)
        
        logger.info(f"LLM text prediction result: prediction={result.prediction} confidence={result.confidence:.4f}")
        
        return LLMPredictionResponse(
            text=request.text,
            prediction=result.prediction,
            confidence=result.confidence,
            explanation=result.explanation,
            risk_factors=result.risk_factors,
            recommendations=result.recommendations,
            model_type="text",
            timestamp=datetime.utcnow(),
            llm_model=llm_analyzer.model_name if llm_analyzer.is_available() else "ml-only"
        )
    except Exception as e:
        logger.error(f"Error in LLM text prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/hybrid", response_model=LLMPredictionResponse)
def predict_hybrid_llm(request: HybridRequest, db: Session = Depends(get_db), http_request: Request = None):
    """Analyze both URL and text using LLM for comprehensive phishing detection."""
    try:
        logger.info(f"LLM hybrid prediction requested: url={request.url} text_length={len(request.text)}")
        
        # Try to use LLM if available, otherwise fallback to ML only
        if llm_analyzer.is_available():
            result = llm_analyzer.analyze_hybrid(request.url, request.text)
        else:
            # Fallback to ML-only analysis
            from app.utils.load_models import model_loader
            ml_result, ml_confidence = model_loader.predict_hybrid(request.url, request.text)
            result = LLMAnalysisResult(
                prediction=ml_result.upper(),
                confidence=ml_confidence,
                explanation="ML-only analysis (LLM unavailable)",
                risk_factors=[],
                recommendations=[]
            )
        
        # Log prediction
        log_llm_prediction(db, url=request.url, text=request.text, result=result, 
                          model_type="hybrid", request=http_request)
        
        logger.info(f"LLM hybrid prediction result: prediction={result.prediction} confidence={result.confidence:.4f}")
        
        return LLMPredictionResponse(
            url=request.url,
            text=request.text,
            prediction=result.prediction,
            confidence=result.confidence,
            explanation=result.explanation,
            risk_factors=result.risk_factors,
            recommendations=result.recommendations,
            model_type="hybrid",
            timestamp=datetime.utcnow(),
            llm_model=llm_analyzer.model_name if llm_analyzer.is_available() else "ml-only"
        )
    except Exception as e:
        logger.error(f"Error in LLM hybrid prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/explain")
def explain_prediction(request: dict):
    """Get detailed explanation for any prediction result."""
    try:
        if not llm_analyzer.is_available():
            raise HTTPException(status_code=503, detail="LLM service unavailable")
        
        # Extract information from request
        url = request.get("url", "")
        text = request.get("text", "")
        original_prediction = request.get("prediction", "")
        
        # Create explanation prompt
        explanation_prompt = f"""
        Explain why this content was classified as {original_prediction}:
        
        URL: {url}
        Text: {text}
        
        Provide a detailed, educational explanation suitable for end users.
        """
        
        # Use LLM to generate explanation
        chain = LLMChain(llm=llm_analyzer.llm, prompt=PromptTemplate(
            input_variables=["content"],
            template="{content}"
        ))
        
        explanation = chain.invoke({"content": explanation_prompt})
        
        return {
            "explanation": explanation,
            "original_prediction": original_prediction,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate explanation")
