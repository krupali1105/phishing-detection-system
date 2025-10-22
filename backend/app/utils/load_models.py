"""
Model loading and prediction utilities.
"""

import joblib
import numpy as np
from typing import Tuple, Dict, Any, List, Optional
import os
import logging
from app.utils.feature_extraction import URLFeatureExtractor, NLPFeatureExtractor, HybridFeatureExtractor

class ModelLoader:
    """Load and manage ML models."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.url_model = None
        self.text_model = None
        self.hybrid_model = None
        self.url_scaler = None
        self.text_scaler = None
        self.hybrid_scaler = None
        self.url_feature_names: Optional[List[str]] = None
        self.text_feature_names: Optional[List[str]] = None
        self.hybrid_feature_names: Optional[List[str]] = None
        self.url_extractor = URLFeatureExtractor()
        self.nlp_extractor = NLPFeatureExtractor()
        self.hybrid_extractor = HybridFeatureExtractor()
        
        # Load models
        self._load_models()
    
    def _load_models(self):
        """Load all trained models and their preprocessing artifacts."""
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Normalize path
        models_dir = os.path.abspath(models_dir)
        
        # Load URL model and artifacts
        try:
            url_model_path = os.path.join(models_dir, 'url_model.pkl')
            url_scaler_path = os.path.join(models_dir, 'url_scaler.pkl')
            url_features_path = os.path.join(models_dir, 'url_feature_names.pkl')
            if os.path.exists(url_model_path):
                self.url_model = joblib.load(url_model_path)
                self.logger.info("URL model loaded")
            if os.path.exists(url_scaler_path):
                self.url_scaler = joblib.load(url_scaler_path)
                self.logger.info("URL scaler loaded")
            if os.path.exists(url_features_path):
                self.url_feature_names = joblib.load(url_features_path)
                self.logger.info("URL feature names loaded")
        except Exception as e:
            self.logger.error(f"Error loading URL artifacts: {e}")
        
        # Load text model and artifacts
        try:
            text_model_path = os.path.join(models_dir, 'text_model.pkl')
            text_scaler_path = os.path.join(models_dir, 'text_scaler.pkl')
            text_features_path = os.path.join(models_dir, 'text_feature_names.pkl')
            tfidf_path = os.path.join(models_dir, 'tfidf_vectorizer.pkl')
            if os.path.exists(text_model_path):
                self.text_model = joblib.load(text_model_path)
                self.logger.info("Text model loaded")
            if os.path.exists(text_scaler_path):
                self.text_scaler = joblib.load(text_scaler_path)
                self.logger.info("Text scaler loaded")
            if os.path.exists(text_features_path):
                self.text_feature_names = joblib.load(text_features_path)
                self.logger.info("Text feature names loaded")
            if os.path.exists(tfidf_path):
                self.nlp_extractor.load_tfidf_vectorizer(tfidf_path)
                self.logger.info("TF-IDF vectorizer loaded")
        except Exception as e:
            self.logger.error(f"Error loading Text artifacts: {e}")
        
        # Load hybrid model and artifacts
        try:
            hybrid_model_path = os.path.join(models_dir, 'hybrid_model.pkl')
            hybrid_scaler_path = os.path.join(models_dir, 'hybrid_scaler.pkl')
            hybrid_features_path = os.path.join(models_dir, 'hybrid_feature_names.pkl')
            if os.path.exists(hybrid_model_path):
                self.hybrid_model = joblib.load(hybrid_model_path)
                self.logger.info("Hybrid model loaded")
            if os.path.exists(hybrid_scaler_path):
                self.hybrid_scaler = joblib.load(hybrid_scaler_path)
                self.logger.info("Hybrid scaler loaded")
            if os.path.exists(hybrid_features_path):
                self.hybrid_feature_names = joblib.load(hybrid_features_path)
                self.logger.info("Hybrid feature names loaded")
        except Exception as e:
            self.logger.error(f"Error loading Hybrid artifacts: {e}")
    
    def predict_url(self, url: str) -> Tuple[str, float]:
        """Predict phishing probability for URL."""
        if self.url_model is None:
            return "Model not available", 0.0
        
        try:
            raw_features = self.url_extractor.extract_features(url)
            if self.url_feature_names:
                ordered = [raw_features.get(name, 0.0) for name in self.url_feature_names]
            else:
                ordered = list(raw_features.values())
            feature_vector = np.array(ordered, dtype=float).reshape(1, -1)
            if self.url_scaler is not None:
                feature_vector = self.url_scaler.transform(feature_vector)
            prediction = self.url_model.predict(feature_vector)[0]
            probability = self.url_model.predict_proba(feature_vector)[0]
            confidence = float(np.max(probability))
            result = "Phishing" if int(prediction) == 1 else "Legitimate"
            return result, confidence
        except Exception as e:
            self.logger.error(f"Error predicting URL: {e}")
            return "Error", 0.0
    
    def predict_text(self, text: str) -> Tuple[str, float]:
        """Predict phishing probability for text."""
        if self.text_model is None:
            return "Model not available", 0.0
        
        try:
            raw_features = self.nlp_extractor.extract_features(text)
            if self.text_feature_names:
                ordered = [raw_features.get(name, 0.0) for name in self.text_feature_names]
            else:
                ordered = list(raw_features.values())
            feature_vector = np.array(ordered, dtype=float).reshape(1, -1)
            if self.text_scaler is not None:
                feature_vector = self.text_scaler.transform(feature_vector)
            prediction = self.text_model.predict(feature_vector)[0]
            probability = self.text_model.predict_proba(feature_vector)[0]
            confidence = float(np.max(probability))
            result = "Phishing" if int(prediction) == 1 else "Legitimate"
            return result, confidence
        except Exception as e:
            self.logger.error(f"Error predicting text: {e}")
            return "Error", 0.0
    
    def predict_hybrid(self, url: str, text: str = None) -> Tuple[str, float]:
        """Predict phishing probability using hybrid model."""
        if self.hybrid_model is None:
            return "Model not available", 0.0
        
        try:
            raw_features = self.hybrid_extractor.extract_features(url, text)
            if self.hybrid_feature_names:
                ordered = [raw_features.get(name, 0.0) for name in self.hybrid_feature_names]
            else:
                ordered = list(raw_features.values())
            feature_vector = np.array(ordered, dtype=float).reshape(1, -1)
            if self.hybrid_scaler is not None:
                feature_vector = self.hybrid_scaler.transform(feature_vector)
            prediction = self.hybrid_model.predict(feature_vector)[0]
            probability = self.hybrid_model.predict_proba(feature_vector)[0]
            confidence = float(np.max(probability))
            result = "Phishing" if int(prediction) == 1 else "Legitimate"
            return result, confidence
        except Exception as e:
            self.logger.error(f"Error predicting hybrid: {e}")
            return "Error", 0.0

# Global model loader instance
model_loader = ModelLoader()

# Convenience functions
def predict_url(url: str) -> Tuple[str, float]:
    """Predict phishing probability for URL."""
    return model_loader.predict_url(url)

def predict_text(text: str) -> Tuple[str, float]:
    """Predict phishing probability for text."""
    return model_loader.predict_text(text)

def predict_hybrid(url: str, text: str = None) -> Tuple[str, float]:
    """Predict phishing probability using hybrid model."""
    return model_loader.predict_hybrid(url, text)
