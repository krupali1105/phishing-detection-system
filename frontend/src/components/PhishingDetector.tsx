"use client";

import React, { useState } from "react";
import ResultCard from "./ResultCard";
import LLMAnalysisCard from "./LLMAnalysisCard";
import AnalyticsDashboard from "./AnalyticsDashboard";
import HistoryPanel from "./HistoryPanel";
import LoadingSpinner from "./LoadingSpinner";
import ModernLoader from "./ModernLoader";
import PageLoading from "./PageLoading";

interface PredictionResult {
  url?: string;
  text?: string;
  prediction: string;
  confidence: number;
  model_type: string;
  timestamp: string;
}

interface LLMResult {
  url?: string;
  text?: string;
  prediction: string;
  confidence: number;
  explanation: string;
  risk_factors: string[];
  recommendations: string[];
  model_type: string;
  timestamp: string;
  llm_model: string;
}

export default function PhishingDetector() {
  const [activeTab, setActiveTab] = useState<'detect' | 'analytics' | 'history'>('detect');
  const [url, setUrl] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [llmResult, setLlmResult] = useState<LLMResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [llmLoading, setLlmLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [modelType, setModelType] = useState<'url' | 'text' | 'hybrid'>('url');
  const [useLLM, setUseLLM] = useState(false);

  const handleUrlCheck = async () => {
    if (!url.trim()) {
      setError("Please enter a URL");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const endpoint = modelType === 'hybrid' ? '/predict/hybrid' : '/predict/url';
      const body = modelType === 'hybrid' 
        ? { url, text: text || undefined }
        : { url };

      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleTextCheck = async () => {
    if (!text.trim()) {
      setError("Please enter text content");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/predict/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleLLMAnalysis = async () => {
    if (useLLM) {
      setLlmLoading(true);
      setError(null);

      try {
        let endpoint = '';
        let body = {};

        if (modelType === 'url') {
          endpoint = '/llm-predict/url';
          body = { url };
        } else if (modelType === 'text') {
          endpoint = '/llm-predict/text';
          body = { text };
        } else {
          endpoint = '/llm-predict/hybrid';
          body = { url, text };
        }

        const response = await fetch(`http://localhost:8000${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setLlmResult(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "LLM analysis failed");
      } finally {
        setLlmLoading(false);
      }
    }
  };

  const handleClear = () => {
    setUrl("");
    setText("");
    setResult(null);
    setLlmResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Page-level loading overlay for LLM analysis */}
      <PageLoading 
        isVisible={llmLoading} 
        message="AI Analysis in Progress..." 
      />
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <h1 className="cursor-pointer text-center sm:text-left text-2xl sm:text-3xl font-bold text-gray-900" onClick={() => setActiveTab('detect')}>
              🛡️ Phishing Detection System
            </h1>

            {/* Tabs */}
            <nav aria-label="Primary" className="-mx-1">
              <div className="overflow-x-auto no-scrollbar sm:block flex justify-center items-center">
                <div className="inline-flex items-center bg-gray-50 border border-gray-200 rounded-full p-2 sm:gap-10 gap-5">
                  <button
                    onClick={() => setActiveTab('detect')}
                    className={`px-2.5 sm:px-5 sm:py-2 py-1.5 rounded-full cursor-pointer text-md font-medium transition ${
                      activeTab === 'detect'
                        ? 'bg-blue-600 text-white shadow'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                    aria-current={activeTab === 'detect' ? 'page' : undefined}
                  >
                    Detection
                  </button>
                  <button
                    onClick={() => setActiveTab('analytics')}
                    className={`px-2.5 sm:px-5 sm:py-2 py-1.5 rounded-full cursor-pointer text-sm font-medium transition ${
                      activeTab === 'analytics'
                        ? 'bg-blue-600 text-white shadow'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                    aria-current={activeTab === 'analytics' ? 'page' : undefined}
                  >
                    Analytics
                  </button>
                  <button
                    onClick={() => setActiveTab('history')}
                    className={`px-2.5 sm:px-5 sm:py-2 py-1.5 rounded-full cursor-pointer text-sm font-medium transition ${
                      activeTab === 'history'
                        ? 'bg-blue-600 text-white shadow'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                    aria-current={activeTab === 'history' ? 'page' : undefined}
                  >
                    History
                  </button>
                </div>
              </div>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 w-full">
        {activeTab === 'detect' && (
          <div className="space-y-6 sm:space-y-8">
            {/* Model Selection */}
            <div className="bg-white rounded-lg shadow p-4 sm:p-6 text-black">
              <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Select Detection Model</h2>
              <div className="flex flex-col sm:flex-row sm:flex-wrap gap-3 sm:gap-6 mb-4">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    value="url"
                    checked={modelType === 'url'}
                    onChange={(e) => setModelType(e.target.value as 'url')}
                    className="mr-2 cursor-pointer"
                  />
                  URL Analysis
                </label>
                <label className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    value="text"
                    checked={modelType === 'text'}
                    onChange={(e) => setModelType(e.target.value as 'text')}
                    className="mr-2 cursor-pointer"
                  />
                  Text Analysis
                </label>
                <label className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    value="hybrid"
                    checked={modelType === 'hybrid'}
                    onChange={(e) => setModelType(e.target.value as 'hybrid')}
                    className="mr-2 cursor-pointer"
                  />
                  Hybrid Analysis
                </label>
              </div>
              
              {/* LLM Toggle */}
              <div className="border-t pt-4">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={useLLM}
                    onChange={(e) => setUseLLM(e.target.checked)}
                    className="mr-2 cursor-pointer"
                  />
                  <span className="font-medium cursor-pointer">🤖 Use AI/LLM Analysis (Enhanced)</span>
                </label>
                <p className="text-sm text-gray-600 mt-1">
                  Enable advanced AI analysis with detailed explanations and risk factors
                </p>
              </div>
            </div>

            {/* Input Forms */}
            <div className="bg-white rounded-lg shadow p-4 sm:p-6 text-black">
              <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Enter Content to Analyze</h2>
              
              {(modelType === 'url' || modelType === 'hybrid') && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    URL
                  </label>
                  <input
                    type="url"
                    placeholder="https://example.com"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              {(modelType === 'text' || modelType === 'hybrid') && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Text Content
                  </label>
                  <textarea
                    placeholder="Enter email content, webpage text, or any suspicious text..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={5}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              )}

              <div className="flex flex-col sm:flex-row gap-3 sm:gap-4">
                <button
                  onClick={async () => {
                    if (useLLM) {
                      await handleLLMAnalysis();
                    } else {
                      if (modelType === 'text') {
                        await handleTextCheck();
                      } else {
                        await handleUrlCheck();
                      }
                    }
                  }}
                  disabled={loading || llmLoading}
                  className="cursor-pointer w-full sm:w-auto bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-h-[40px]"
                >
                  {loading ? (
                    <ModernLoader size="sm" text="Analyzing..." variant="spinner" />
                  ) : llmLoading ? (
                    <ModernLoader size="sm" text="AI Analyzing..." variant="wave" />
                  ) : useLLM ? (
                    "🤖 AI Analyze"
                  ) : (
                    "Analyze"
                  )}
                </button>
                <button
                  onClick={handleClear}
                  className="cursor-pointer w-full sm:w-auto bg-gray-500 text-white px-6 py-2 rounded-md hover:bg-gray-600"
                >
                  Clear
                </button>
              </div>

              {error && (
                <div className="mt-4 p-3 sm:p-4 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
                  {error}
                </div>
              )}
            </div>

            {/* Results */}
            {result && !useLLM && <ResultCard result={result} />}
            {llmResult && useLLM && <LLMAnalysisCard result={llmResult} />}
          </div>
        )}

        {activeTab === 'analytics' && <AnalyticsDashboard />}
        {activeTab === 'history' && <HistoryPanel />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-8 sm:mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-500 text-sm sm:text-base">
            <p>© 2024 Phishing Detection System. Powered by AI and Machine Learning.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
