"""
Analytics and history endpoints for the phishing detection system.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db import get_db, PredictionLog, AnalyticsData
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import logging

router = APIRouter(prefix="/analytics", tags=["Analytics"])
logger = logging.getLogger(__name__)

class PredictionHistory(BaseModel):
    id: int
    url: Optional[str]
    text: Optional[str]
    prediction: str
    confidence: float
    model_type: str
    timestamp: datetime
    ip_address: Optional[str]

class AnalyticsSummary(BaseModel):
    total_predictions: int
    phishing_count: int
    legitimate_count: int
    phishing_percentage: float
    avg_confidence: float
    model_usage: dict

class DailyStats(BaseModel):
    date: str
    total_predictions: int
    phishing_count: int
    legitimate_count: int
    avg_confidence: float

@router.get("/history", response_model=List[PredictionHistory])
def get_prediction_history(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    model_type: Optional[str] = Query(None),
    prediction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get prediction history with optional filters."""
    try:
        query = db.query(PredictionLog)
        
        if model_type:
            query = query.filter(PredictionLog.model_type == model_type)
        
        if prediction:
            query = query.filter(PredictionLog.prediction == prediction)
        
        predictions = query.order_by(desc(PredictionLog.timestamp)).offset(offset).limit(limit).all()
        
        return [
            PredictionHistory(
                id=p.id,
                url=p.url,
                text=p.text,
                prediction=p.prediction,
                confidence=p.confidence,
                model_type=p.model_type,
                timestamp=p.timestamp,
                ip_address=p.ip_address
            )
            for p in predictions
        ]
    except Exception as e:
        logger.error(f"Error fetching prediction history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(db: Session = Depends(get_db)):
    """Get overall analytics summary."""
    try:
        # Total predictions
        total_predictions = db.query(PredictionLog).count()
        
        # Phishing vs legitimate counts
        phishing_count = db.query(PredictionLog).filter(PredictionLog.prediction == "Phishing").count()
        legitimate_count = db.query(PredictionLog).filter(PredictionLog.prediction == "Legitimate").count()
        
        # Average confidence
        avg_confidence_result = db.query(func.avg(PredictionLog.confidence)).scalar()
        avg_confidence = float(avg_confidence_result) if avg_confidence_result else 0.0
        
        # Model usage statistics
        model_usage = {}
        for model_type in ["url", "text", "hybrid"]:
            count = db.query(PredictionLog).filter(PredictionLog.model_type == model_type).count()
            model_usage[model_type] = count
        
        phishing_percentage = (phishing_count / total_predictions * 100) if total_predictions > 0 else 0.0
        
        return AnalyticsSummary(
            total_predictions=total_predictions,
            phishing_count=phishing_count,
            legitimate_count=legitimate_count,
            phishing_percentage=phishing_percentage,
            avg_confidence=avg_confidence,
            model_usage=model_usage
        )
    except Exception as e:
        logger.error(f"Error fetching analytics summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/daily-stats", response_model=List[DailyStats])
def get_daily_stats(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get daily statistics for the last N days."""
    try:
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)
        
        daily_stats = []
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Get predictions for this date
            day_start = datetime.combine(current_date, datetime.min.time())
            day_end = datetime.combine(current_date, datetime.max.time())
            
            day_predictions = db.query(PredictionLog).filter(
                PredictionLog.timestamp >= day_start,
                PredictionLog.timestamp <= day_end
            ).all()
            
            total_predictions = len(day_predictions)
            phishing_count = sum(1 for p in day_predictions if p.prediction == "Phishing")
            legitimate_count = sum(1 for p in day_predictions if p.prediction == "Legitimate")
            
            avg_confidence = 0.0
            if day_predictions:
                avg_confidence = sum(p.confidence for p in day_predictions) / len(day_predictions)
            
            daily_stats.append(DailyStats(
                date=current_date.strftime("%Y-%m-%d"),
                total_predictions=total_predictions,
                phishing_count=phishing_count,
                legitimate_count=legitimate_count,
                avg_confidence=avg_confidence
            ))
        
        return daily_stats
    except Exception as e:
        logger.error(f"Error fetching daily stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/top-phishing-urls")
def get_top_phishing_urls(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get most frequently detected phishing URLs."""
    try:
        phishing_urls = db.query(
            PredictionLog.url,
            func.count(PredictionLog.id).label('count'),
            func.avg(PredictionLog.confidence).label('avg_confidence')
        ).filter(
            PredictionLog.prediction == "Phishing",
            PredictionLog.url.isnot(None)
        ).group_by(PredictionLog.url).order_by(desc('count')).limit(limit).all()
        
        return [
            {
                "url": url,
                "count": count,
                "avg_confidence": float(avg_confidence)
            }
            for url, count, avg_confidence in phishing_urls
        ]
    except Exception as e:
        logger.error(f"Error fetching top phishing URLs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/model-performance")
def get_model_performance(db: Session = Depends(get_db)):
    """Get performance metrics for each model."""
    try:
        models = ["url", "text", "hybrid"]
        performance = {}
        
        for model_type in models:
            predictions = db.query(PredictionLog).filter(PredictionLog.model_type == model_type).all()
            
            if predictions:
                total = len(predictions)
                phishing_count = sum(1 for p in predictions if p.prediction == "Phishing")
                avg_confidence = sum(p.confidence for p in predictions) / total
                
                performance[model_type] = {
                    "total_predictions": total,
                    "phishing_count": phishing_count,
                    "legitimate_count": total - phishing_count,
                    "phishing_percentage": (phishing_count / total) * 100,
                    "avg_confidence": avg_confidence
                }
            else:
                performance[model_type] = {
                    "total_predictions": 0,
                    "phishing_count": 0,
                    "legitimate_count": 0,
                    "phishing_percentage": 0.0,
                    "avg_confidence": 0.0
                }
        
        return performance
    except Exception as e:
        logger.error(f"Error fetching model performance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
