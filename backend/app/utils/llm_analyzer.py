"""
LLM-based phishing analysis using Ollama and LangChain.
Provides enhanced text understanding and explainable predictions.
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import requests
import joblib
from langchain.prompts import PromptTemplate  # type: ignore
from langchain.chains import LLMChain  # type: ignore
from langchain.schema import BaseOutputParser  # type: ignore
from langchain_ollama import OllamaLLM  # type: ignore
from app.utils.feature_extraction import URLFeatureExtractor

logger = logging.getLogger(__name__)

@dataclass
class LLMAnalysisResult:
    """Result from LLM analysis."""
    prediction: str  # "PHISHING" or "LEGITIMATE"
    confidence: float  # 0.0 to 1.0
    explanation: str
    risk_factors: List[str]
    recommendations: List[str]

class PhishingAnalysisParser(BaseOutputParser):
    """Parse LLM output for phishing analysis."""
    
    def parse(self, text: str) -> Dict:
        """Parse LLM response into structured format."""
        try:
            # Try to extract JSON from response
            if "{" in text and "}" in text:
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                return json.loads(json_str)
            else:
                # Fallback parsing
                return self._fallback_parse(text)
        except Exception as e:
            logger.warning(f"Failed to parse LLM response: {e}")
            return self._fallback_parse(text)
    
    def _fallback_parse(self, text: str) -> Dict:
        """Fallback parsing when JSON extraction fails."""
        text_lower = text.lower()
        
        # Determine prediction
        if any(word in text_lower for word in ["phishing", "suspicious", "malicious", "dangerous"]):
            prediction = "PHISHING"
        elif any(word in text_lower for word in ["legitimate", "safe", "clean", "normal"]):
            prediction = "LEGITIMATE"
        else:
            prediction = "UNKNOWN"
        
        # Extract confidence (look for percentages or scores)
        confidence = 0.5  # Default
        if "%" in text:
            try:
                import re
                percentages = re.findall(r'(\d+)%', text)
                if percentages:
                    confidence = float(percentages[0]) / 100.0
            except:
                pass
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "explanation": text[:500],  # Truncate long explanations
            "risk_factors": [],
            "recommendations": []
        }

class LLMPhishingAnalyzer:
    """LLM-based phishing detection analyzer."""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        """
        Initialize LLM analyzer.
        
        Args:
            model_name: Ollama model to use (llama2, mistral, etc.)
            base_url: Ollama server URL
        """
        self.model_name = model_name
        self.base_url = base_url
        self.llm = None
        self.parser = PhishingAnalysisParser()
        
        # Initialize LLM
        self._initialize_llm()
        
        # Create prompts
        self._create_prompts()
    
    def _initialize_llm(self):
        """Initialize the LLM connection."""
        try:
            self.llm = OllamaLLM(
                model="llama2",
                base_url=self.base_url,
                temperature=0.1,  # Low temperature for consistent results
                top_p=0.9
            )
            logger.info(f"LLM initialized with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            self.llm = None
    
    def _create_prompts(self):
        """Create prompt templates for different analysis types."""
        
        # URL Analysis Prompt
        self.url_prompt = PromptTemplate(
            input_variables=["url"],
            template="""
You are a cybersecurity expert analyzing URLs for phishing indicators.

URL: {url}

Important:
- If ANY phishing indicator is present, prediction MUST be "PHISHING".
- Do NOT classify as "LEGITIMATE" unless you are certain the link is safe.
- When in doubt, default to "PHISHING".

Analyze this URL and provide a JSON response with:
1. prediction: "PHISHING" or "LEGITIMATE"
2. confidence: score from 0.0 to 1.0
3. explanation: detailed reasoning
4. risk_factors: list of suspicious elements found
5. recommendations: security advice

Consider these factors:
- Domain reputation and age
- Suspicious subdomains or paths
- URL shortening services
- Typosquatting attempts
- HTTPS vs HTTP
- Suspicious TLDs (.tk, .ml, .ga, etc.)
- IP addresses instead of domains
- Special characters and encoding

Response format (JSON only):
{{
    "prediction": "PHISHING",
    "confidence": 0.85,
    "explanation": "This URL shows multiple red flags...",
    "risk_factors": ["suspicious domain", "http instead of https"],
    "recommendations": ["Avoid clicking", "Report to security team"]
}}
"""
        )
        
        # Text Analysis Prompt
        self.text_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
You are a cybersecurity expert analyzing text content for phishing indicators.

Text: {text}

Analyze this text and provide a JSON response with:
1. prediction: "PHISHING" or "LEGITIMATE"
2. confidence: score from 0.0 to 1.0
3. explanation: detailed reasoning
4. risk_factors: list of suspicious elements found
5. recommendations: security advice

Consider these factors:
- Urgency and pressure tactics
- Authority impersonation
- Suspicious requests (passwords, payments)
- Grammar and spelling errors
- Emotional manipulation
- Threats or consequences
- Unusual formatting or characters
- Social engineering techniques

Response format (JSON only):
{{
    "prediction": "PHISHING",
    "confidence": 0.90,
    "explanation": "This text contains classic phishing tactics...",
    "risk_factors": ["urgency tactics", "authority impersonation"],
    "recommendations": ["Do not respond", "Verify sender identity"]
}}
"""
        )
        
        # Hybrid Analysis Prompt
        self.hybrid_prompt = PromptTemplate(
            input_variables=["url", "text"],
            template="""
You are a cybersecurity expert analyzing both URL and text content for phishing indicators.

URL: {url}
Text: {text}

Analyze both elements together and provide a JSON response with:
1. prediction: "PHISHING" or "LEGITIMATE"
2. confidence: score from 0.0 to 1.0
3. explanation: detailed reasoning considering both URL and text
4. risk_factors: list of suspicious elements found in both
5. recommendations: comprehensive security advice

Consider:
- Consistency between URL and text content
- Combined risk factors
- Cross-referencing suspicious elements
- Overall threat assessment

Response format (JSON only):
{{
    "prediction": "PHISHING",
    "confidence": 0.95,
    "explanation": "Both URL and text show coordinated phishing attempts...",
    "risk_factors": ["suspicious domain", "urgency tactics", "authority impersonation"],
    "recommendations": ["Avoid interaction", "Report to security", "Educate users"]
}}
"""
        )
    
    def analyze_url(self, url: str) -> LLMAnalysisResult:
        """Analyze URL using LLM."""
        if not self.llm:
            return self._fallback_result("LLM not available")
        
        try:
            chain = LLMChain(llm=self.llm, prompt=self.url_prompt)
            raw_output = chain.invoke({"url": url})
            result = self.parser.parse(raw_output)

            # Enforce stricter phishing bias
            if result.get("prediction") == "LEGITIMATE" and result.get("confidence", 0.5) < 0.9:
                result["prediction"] = "PHISHING"
            
            return LLMAnalysisResult(
                prediction=result.get("prediction", "UNKNOWN"),
                confidence=result.get("confidence", 0.5),
                explanation=result.get("explanation", "No explanation available"),
                risk_factors=result.get("risk_factors", []),
                recommendations=result.get("recommendations", [])
            )
        except Exception as e:
            logger.error(f"LLM URL analysis failed: {e}")
            return self._fallback_result(f"Analysis failed: {str(e)}")
    
    def analyze_text(self, text: str) -> LLMAnalysisResult:
        """Analyze text using LLM."""
        if not self.llm:
            return self._fallback_result("LLM not available")
        
        try:
            chain = LLMChain(llm=self.llm, prompt=self.text_prompt, output_parser=self.parser)
            result = chain.invoke({"text":text})
            
            return LLMAnalysisResult(
                prediction=result.get("prediction", "UNKNOWN"),
                confidence=result.get("confidence", 0.5),
                explanation=result.get("explanation", "No explanation available"),
                risk_factors=result.get("risk_factors", []),
                recommendations=result.get("recommendations", [])
            )
        except Exception as e:
            logger.error(f"LLM text analysis failed: {e}")
            return self._fallback_result(f"Analysis failed: {str(e)}")
    
    def analyze_hybrid(self, url: str, text: str) -> LLMAnalysisResult:
        """Analyze both URL and text using LLM."""
        if not self.llm:
            return self._fallback_result("LLM not available")
        
        try:
            chain = LLMChain(llm=self.llm, prompt=self.hybrid_prompt, output_parser=self.parser)
            result = chain.invoke({"url": url, "text":text})
            
            return LLMAnalysisResult(
                prediction=result.get("prediction", "UNKNOWN"),
                confidence=result.get("confidence", 0.5),
                explanation=result.get("explanation", "No explanation available"),
                risk_factors=result.get("risk_factors", []),
                recommendations=result.get("recommendations", [])
            )
        except Exception as e:
            logger.error(f"LLM hybrid analysis failed: {e}")
            return self._fallback_result(f"Analysis failed: {str(e)}")
    
    def _fallback_result(self, error_msg: str) -> LLMAnalysisResult:
        """Return fallback result when LLM is unavailable."""
        return LLMAnalysisResult(
            prediction="UNKNOWN",
            confidence=0.0,
            explanation=f"LLM analysis unavailable: {error_msg}",
            risk_factors=[],
            recommendations=["Use traditional ML analysis", "Check LLM service status"]
        )
    
    def is_available(self) -> bool:
        """Check if LLM service is available."""
        if not self.llm:
            return False
        
        try:
            # Test connection
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except:
            return []

# Global LLM analyzer instance
llm_analyzer = LLMPhishingAnalyzer()

def final_url_analysis(url: str):
    """Combined ML + LLM analysis for URL."""
    try:
        # Step 1: Run ML model using the same feature extraction as the main system
        from app.utils.load_models import model_loader
        
        # Use the existing model loader to get consistent predictions
        ml_result, ml_confidence = model_loader.predict_url(url)
        ml_is_phishing = ml_result.lower() == "phishing"
        
        # Step 2: Run LLM analysis
        llm_result = llm_analyzer.analyze_url(url)
        
        # Step 3: Combine results (weighted average)
        if ml_is_phishing and llm_result.prediction.upper() == "PHISHING":
            # Both agree on phishing - high confidence
            return "PHISHING", max(0.9, (ml_confidence + llm_result.confidence) / 2)
        elif ml_is_phishing or llm_result.prediction.upper() == "PHISHING":
            # One suggests phishing - medium confidence
            return "PHISHING", max(0.7, (ml_confidence + llm_result.confidence) / 2)
        else:
            # Both agree on legitimate - use average confidence
            return "LEGITIMATE", (ml_confidence + llm_result.confidence) / 2
            
    except Exception as e:
        logger.error(f"Error in final_url_analysis: {e}")
        # Fallback to just LLM if ML fails
        try:
            llm_result = llm_analyzer.analyze_url(url)
            return llm_result.prediction, llm_result.confidence
        except Exception as llm_error:
            logger.error(f"LLM analysis also failed: {llm_error}")
            return "LEGITIMATE", 0.5  # Default safe fallback

