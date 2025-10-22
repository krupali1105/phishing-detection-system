"""
Master script to train all phishing detection models.
Runs URL, text, and hybrid model training sequentially.
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from train_url_model import train_url_model
from train_text_model import train_text_model
from train_hybrid import train_hybrid_model

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('training.log'),
            logging.StreamHandler()
        ]
    )

def train_all_models():
    """Train all phishing detection models."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting comprehensive model training...")
    start_time = datetime.now()
    
    try:
        # Train URL model
        logger.info("=" * 50)
        logger.info("TRAINING URL MODEL")
        logger.info("=" * 50)
        url_model, url_scaler, url_features = train_url_model()
        logger.info("URL model training completed successfully")
        
        # Train text model
        logger.info("=" * 50)
        logger.info("TRAINING TEXT MODEL")
        logger.info("=" * 50)
        text_model, text_vectorizer, text_features = train_text_model()
        logger.info("Text model training completed successfully")
        
        # Train hybrid model
        logger.info("=" * 50)
        logger.info("TRAINING HYBRID MODEL")
        logger.info("=" * 50)
        hybrid_model, hybrid_scaler, hybrid_features = train_hybrid_model()
        logger.info("Hybrid model training completed successfully")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("=" * 50)
        logger.info("TRAINING SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Total training time: {duration}")
        logger.info(f"URL model features: {len(url_features)}")
        logger.info(f"Text model features: {len(text_features)}")
        logger.info(f"Hybrid model features: {len(hybrid_features)}")
        logger.info("All models trained successfully!")
        
        return {
            'url_model': url_model,
            'text_model': text_model,
            'hybrid_model': hybrid_model,
            'url_features': url_features,
            'text_features': text_features,
            'hybrid_features': hybrid_features
        }
        
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise

if __name__ == "__main__":
    train_all_models()
