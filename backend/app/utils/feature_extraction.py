"""
Feature extraction utilities for phishing detection.
Extracts URL lexical features, WHOIS features, and NLP features.
"""

import re
import urllib.parse
import socket
import ssl
from datetime import datetime
import whois
import requests
from bs4 import BeautifulSoup
import numpy as np
from typing import Dict, List, Optional, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModel
import torch
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Ensure punkt_tab is available for newer NLTK tokenizer requirements
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class URLFeatureExtractor:
    """Extract lexical features from URLs."""
    
    def __init__(self):
        self.suspicious_keywords = [
            'secure', 'account', 'update', 'verify', 'confirm', 'login',
            'bank', 'paypal', 'amazon', 'apple', 'microsoft', 'google',
            'facebook', 'twitter', 'instagram', 'linkedin', 'netflix',
            'suspicious', 'phishing', 'scam', 'fraud', 'fake'
        ]
        
        self.suspicious_tlds = [
            '.tk', '.ml', '.ga', '.cf', '.click', '.download', '.review'
        ]
    
    def extract_features(self, url: str) -> Dict[str, float]:
        """Extract comprehensive URL features."""
        features = {}
        
        # Basic URL features
        features.update(self._extract_basic_features(url))
        
        # Domain features
        features.update(self._extract_domain_features(url))
        
        # Path features
        features.update(self._extract_path_features(url))
        
        # Query features
        features.update(self._extract_query_features(url))
        
        # Suspicious patterns
        features.update(self._extract_suspicious_features(url))
        
        return features
    
    def _extract_basic_features(self, url: str) -> Dict[str, float]:
        """Extract basic URL characteristics."""
        features = {}
        
        # URL length
        features['url_length'] = len(url)
        
        # Number of dots
        features['num_dots'] = url.count('.')
        
        # Number of hyphens
        features['num_hyphens'] = url.count('-')
        
        # Number of underscores
        features['num_underscores'] = url.count('_')
        
        # Number of slashes
        features['num_slashes'] = url.count('/')
        
        # Number of digits
        features['num_digits'] = sum(c.isdigit() for c in url)
        
        # Number of special characters
        special_chars = "!@#$%^&*()+=[]{}|;:,.<>?"
        features['num_special_chars'] = sum(c in special_chars for c in url)
        
        return features
    
    def _extract_domain_features(self, url: str) -> Dict[str, float]:
        """Extract domain-related features."""
        features = {}
        
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()
            
            # Domain length
            features['domain_length'] = len(domain)
            
            # Number of subdomains
            features['num_subdomains'] = len(domain.split('.')) - 2
            
            # Has IP address
            features['has_ip'] = 1.0 if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain) else 0.0
            
            # Has HTTPS
            features['has_https'] = 1.0 if parsed.scheme == 'https' else 0.0
            
            # TLD length
            tld = domain.split('.')[-1] if '.' in domain else ''
            features['tld_length'] = len(tld)
            
            # Suspicious TLD
            features['suspicious_tld'] = 1.0 if any(tld.endswith(susp_tld) for susp_tld in self.suspicious_tlds) else 0.0
            
        except Exception:
            # Default values if parsing fails
            features.update({
                'domain_length': 0.0,
                'num_subdomains': 0.0,
                'has_ip': 0.0,
                'has_https': 0.0,
                'tld_length': 0.0,
                'suspicious_tld': 0.0
            })
        
        return features
    
    def _extract_path_features(self, url: str) -> Dict[str, float]:
        """Extract path-related features."""
        features = {}
        
        try:
            parsed = urllib.parse.urlparse(url)
            path = parsed.path
            
            # Path length
            features['path_length'] = len(path)
            
            # Number of directories
            features['num_directories'] = len([d for d in path.split('/') if d])
            
            # Has file extension
            features['has_file_extension'] = 1.0 if '.' in path.split('/')[-1] else 0.0
            
            # Suspicious keywords in path
            path_lower = path.lower()
            features['suspicious_path_keywords'] = sum(1 for keyword in self.suspicious_keywords if keyword in path_lower)
            
        except Exception:
            features.update({
                'path_length': 0.0,
                'num_directories': 0.0,
                'has_file_extension': 0.0,
                'suspicious_path_keywords': 0.0
            })
        
        return features
    
    def _extract_query_features(self, url: str) -> Dict[str, float]:
        """Extract query parameter features."""
        features = {}
        
        try:
            parsed = urllib.parse.urlparse(url)
            query = parsed.query
            
            # Query length
            features['query_length'] = len(query)
            
            # Number of parameters
            features['num_params'] = len(query.split('&')) if query else 0
            
            # Suspicious keywords in query
            query_lower = query.lower()
            features['suspicious_query_keywords'] = sum(1 for keyword in self.suspicious_keywords if keyword in query_lower)
            
        except Exception:
            features.update({
                'query_length': 0.0,
                'num_params': 0.0,
                'suspicious_query_keywords': 0.0
            })
        
        return features
    
    def _extract_suspicious_features(self, url: str) -> Dict[str, float]:
        """Extract suspicious pattern features."""
        features = {}
        
        url_lower = url.lower()
        
        # Suspicious keywords in URL
        features['suspicious_keywords'] = sum(1 for keyword in self.suspicious_keywords if keyword in url_lower)
        
        # URL shortening services
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'short.link']
        features['is_shortened'] = 1.0 if any(shortener in url_lower for shortener in shorteners) else 0.0
        
        # Repeated characters
        features['has_repeated_chars'] = 1.0 if re.search(r'(.)\1{2,}', url) else 0.0
        
        # Mixed case
        features['has_mixed_case'] = 1.0 if any(c.islower() for c in url) and any(c.isupper() for c in url) else 0.0
        
        return features


class WHOISFeatureExtractor:
    """Extract WHOIS features from domain."""
    
    def extract_features(self, url: str) -> Dict[str, float]:
        """Extract WHOIS features."""
        features = {}
        
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
            whois_info = whois.whois(domain)
            
            # Domain age
            if whois_info.creation_date:
                if isinstance(whois_info.creation_date, list):
                    creation_date = whois_info.creation_date[0]
                else:
                    creation_date = whois_info.creation_date
                
                age_days = (datetime.now() - creation_date).days
                features['domain_age_days'] = float(age_days)
            else:
                features['domain_age_days'] = 0.0
            
            # Registrar
            features['has_registrar'] = 1.0 if whois_info.registrar else 0.0
            
            # Country
            features['has_country'] = 1.0 if whois_info.country else 0.0
            
        except Exception:
            # Default values if WHOIS lookup fails
            features.update({
                'domain_age_days': 0.0,
                'has_registrar': 0.0,
                'has_country': 0.0
            })
        
        return features


class NLPFeatureExtractor:
    """Extract NLP features from text content."""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer = None
        self.model = None
        self.tfidf_vectorizer = None
        
    def load_bert_model(self, model_name: str = "bert-base-uncased"):
        """Load BERT model for embeddings."""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.eval()
        except Exception as e:
            print(f"Error loading BERT model: {e}")
    
    def load_tfidf_vectorizer(self, vectorizer_path: str):
        """Load pre-trained TF-IDF vectorizer."""
        try:
            self.tfidf_vectorizer = joblib.load(vectorizer_path)
        except Exception as e:
            print(f"Error loading TF-IDF vectorizer: {e}")
    
    def extract_text_from_url(self, url: str) -> str:
        """Extract text content from URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit text length
            
        except Exception as e:
            print(f"Error extracting text from URL: {e}")
            return ""
    
    def extract_features(self, text: str) -> Dict[str, float]:
        """Extract comprehensive NLP features."""
        features = {}
        
        # Basic text features
        features.update(self._extract_basic_text_features(text))
        
        # TF-IDF features
        if self.tfidf_vectorizer:
            features.update(self._extract_tfidf_features(text))
        
        # BERT embeddings
        if self.tokenizer and self.model:
            features.update(self._extract_bert_features(text))
        
        return features
    
    def _extract_basic_text_features(self, text: str) -> Dict[str, float]:
        """Extract basic text characteristics."""
        features = {}
        
        # Text length
        features['text_length'] = len(text)
        
        # Word count
        words = word_tokenize(text.lower())
        features['word_count'] = len(words)
        
        # Average word length
        if words:
            features['avg_word_length'] = sum(len(word) for word in words) / len(words)
        else:
            features['avg_word_length'] = 0.0
        
        # Stop word ratio
        stop_word_count = sum(1 for word in words if word in self.stop_words)
        features['stop_word_ratio'] = stop_word_count / len(words) if words else 0.0
        
        # Special character ratio
        special_chars = "!@#$%^&*()+=[]{}|;:,.<>?"
        special_char_count = sum(1 for char in text if char in special_chars)
        features['special_char_ratio'] = special_char_count / len(text) if text else 0.0
        
        # Suspicious keywords
        suspicious_keywords = [
            'urgent', 'immediate', 'verify', 'confirm', 'account', 'security',
            'suspended', 'locked', 'expired', 'update', 'click', 'here',
            'phishing', 'scam', 'fraud', 'fake', 'suspicious'
        ]
        
        text_lower = text.lower()
        features['suspicious_keywords'] = sum(1 for keyword in suspicious_keywords if keyword in text_lower)
        
        return features
    
    def _extract_tfidf_features(self, text: str) -> Dict[str, float]:
        """Extract TF-IDF features."""
        features = {}
        
        try:
            tfidf_matrix = self.tfidf_vectorizer.transform([text])
            tfidf_features = tfidf_matrix.toarray()[0]
            
            # Use top TF-IDF features
            top_indices = np.argsort(tfidf_features)[-50:]  # Top 50 features
            
            for i, idx in enumerate(top_indices):
                features[f'tfidf_{i}'] = tfidf_features[idx]
                
        except Exception as e:
            print(f"Error extracting TF-IDF features: {e}")
        
        return features
    
    def _extract_bert_features(self, text: str) -> Dict[str, float]:
        """Extract BERT embeddings."""
        features = {}
        
        try:
            # Tokenize and encode
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
            
            # Use first 10 dimensions of BERT embeddings
            for i in range(min(10, len(embeddings))):
                features[f'bert_{i}'] = float(embeddings[i])
                
        except Exception as e:
            print(f"Error extracting BERT features: {e}")
        
        return features


class HybridFeatureExtractor:
    """Combine URL, WHOIS, and NLP features."""
    
    def __init__(self):
        self.url_extractor = URLFeatureExtractor()
        self.whois_extractor = WHOISFeatureExtractor()
        self.nlp_extractor = NLPFeatureExtractor()
    
    def extract_features(self, url: str, text: Optional[str] = None) -> Dict[str, float]:
        """Extract all features for hybrid model."""
        features = {}
        
        # URL features
        features.update(self.url_extractor.extract_features(url))
        
        # WHOIS features
        features.update(self.whois_extractor.extract_features(url))
        
        # NLP features
        if text is None:
            text = self.nlp_extractor.extract_text_from_url(url)
        
        if text:
            features.update(self.nlp_extractor.extract_features(text))
        
        return features
