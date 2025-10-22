import React from "react";

interface LLMAnalysisResult {
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

export default function LLMAnalysisCard({ result }: { result: LLMAnalysisResult }) {
  const isPhishing = result.prediction.toLowerCase() === "phishing";
  const confidencePercentage = Math.round(result.confidence * 100);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-900">🤖 LLM Analysis Result</h2>
        <div className="flex items-center space-x-2">
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${
            isPhishing 
              ? 'bg-red-100 text-red-800' 
              : 'bg-green-100 text-green-800'
          }`}>
            {isPhishing ? "⚠️ Phishing Detected" : "✅ Legitimate"}
          </div>
          <div className="text-xs text-gray-500">
            Powered by {result.llm_model}
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {/* Confidence Bar */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">AI Confidence Level</span>
            <span className="text-sm font-bold text-gray-900">{confidencePercentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                isPhishing ? 'bg-red-500' : 'bg-green-500'
              }`}
              style={{ width: `${confidencePercentage}%` }}
            ></div>
          </div>
        </div>

        {/* AI Explanation */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-semibold text-gray-900 mb-2">🧠 AI Analysis</h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            {result.explanation}
          </p>
        </div>

        {/* Risk Factors */}
        {result.risk_factors.length > 0 && (
          <div className="bg-red-50 p-4 rounded-lg">
            <h3 className="font-semibold text-red-900 mb-2">🚨 Risk Factors Identified</h3>
            <ul className="list-disc list-inside space-y-1">
              {result.risk_factors.map((factor, index) => (
                <li key={index} className="text-sm text-red-700">
                  {factor}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {result.recommendations.length > 0 && (
          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="font-semibold text-green-900 mb-2">💡 Security Recommendations</h3>
            <ul className="list-disc list-inside space-y-1">
              {result.recommendations.map((recommendation, index) => (
                <li key={index} className="text-sm text-green-700">
                  {recommendation}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Analysis Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-2">Analysis Details</h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="font-medium text-gray-700">Model Type:</span>
                <span className="ml-2 text-gray-900 capitalize">{result.model_type}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">LLM Model:</span>
                <span className="ml-2 text-gray-900">{result.llm_model}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Timestamp:</span>
                <span className="ml-2 text-gray-900">
                  {new Date(result.timestamp).toISOString().replace('T', ' ').slice(0, 19)}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-2">Risk Assessment</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center">
                <span className="font-medium text-gray-700">Risk Level:</span>
                <span className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
                  confidencePercentage >= 80 
                    ? 'bg-red-100 text-red-800' 
                    : confidencePercentage >= 60 
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-green-100 text-green-800'
                }`}>
                  {confidencePercentage >= 80 ? 'High' : confidencePercentage >= 60 ? 'Medium' : 'Low'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-700">AI Recommendation:</span>
                <span className="ml-2 text-gray-900">
                  {isPhishing 
                    ? 'Avoid this content' 
                    : 'This appears to be safe'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Content Preview */}
        {(result.url || result.text) && (
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-2">Analyzed Content</h3>
            <div className="text-sm text-gray-700">
              {result.url && (
                <div className="mb-2">
                  <span className="font-medium">URL:</span>
                  <div className="mt-1 p-2 bg-white rounded border font-mono text-xs break-all">
                    {result.url}
                  </div>
                </div>
              )}
              {result.text && (
                <div>
                  <span className="font-medium">Text:</span>
                  <div className="mt-1 p-2 bg-white rounded border text-xs max-h-32 overflow-y-auto">
                    {result.text.length > 200 
                      ? `${result.text.substring(0, 200)}...` 
                      : result.text}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-4 pt-4">
          <button
            onClick={() => {
              if (typeof window !== 'undefined' && result.url) {
                window.open(result.url, '_blank');
              }
            }}
            disabled={!result.url}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Visit URL
          </button>
          <button
            onClick={() => {
              if (typeof window !== 'undefined' && navigator.clipboard) {
                navigator.clipboard.writeText(result.url || result.text || '');
              }
            }}
            className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700"
          >
            Copy Content
          </button>
        </div>
      </div>
    </div>
  );
}
