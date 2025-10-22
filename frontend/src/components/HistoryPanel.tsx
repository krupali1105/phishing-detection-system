"use client";

import React, { useState, useEffect, useCallback } from "react";
import ModernLoader from "./ModernLoader";
import SkeletonLoader from "./SkeletonLoader";
import EmptyState from "./EmptyState";

interface PredictionHistory {
  id: number;
  url?: string;
  text?: string;
  prediction: string;
  confidence: number;
  model_type: string;
  timestamp: string;
  ip_address?: string;
}

export default function HistoryPanel() {
  const [history, setHistory] = useState<PredictionHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    model_type: "",
    prediction: "",
    limit: 50,
  });

  const fetchHistory = useCallback(async () => {
    try {
      setLoading(true);

      const params = new URLSearchParams();
      if (filters.model_type) params.append("model_type", filters.model_type);
      if (filters.prediction) params.append("prediction", filters.prediction);
      params.append("limit", filters.limit.toString());

      const response = await fetch(
        `http://localhost:8000/analytics/history?${params}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setHistory(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch history");
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const clearFilters = () => {
    setFilters({
      model_type: "",
      prediction: "",
      limit: 50,
    });
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-center items-center h-32">
          <ModernLoader size="lg" text="Loading History..." variant="spinner" />
        </div>
        <SkeletonLoader variant="list" count={5} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Prediction History
        </h1>
        <p className="text-gray-600">
          View and filter past phishing detection results
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Model Type
            </label>
            <select
              value={filters.model_type}
              onChange={(e) =>
                setFilters({ ...filters, model_type: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Models</option>
              <option value="url">URL Analysis</option>
              <option value="text">Text Analysis</option>
              <option value="hybrid">Hybrid Analysis</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Prediction
            </label>
            <select
              value={filters.prediction}
              onChange={(e) =>
                setFilters({ ...filters, prediction: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Results</option>
              <option value="Phishing">Phishing</option>
              <option value="Legitimate">Legitimate</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Limit
            </label>
            <select
              value={filters.limit}
              onChange={(e) =>
                setFilters({ ...filters, limit: parseInt(e.target.value) })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={25}>25 results</option>
              <option value={50}>50 results</option>
              <option value={100}>100 results</option>
              <option value={200}>200 results</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={clearFilters}
              className="cursor-pointer w-full bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">
            Showing {history.length} prediction{history.length !== 1 ? "s" : ""}
          </span>
          <button
            onClick={fetchHistory}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Content
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Result
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Time
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {history.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="max-w-xs">
                      {item.url ? (
                        <div>
                          <div className="text-sm font-medium text-gray-900 truncate">
                            {item.url}
                          </div>
                          <div className="text-xs text-gray-500">
                            URL Analysis
                          </div>
                        </div>
                      ) : item.text ? (
                        <div>
                          <div className="text-sm text-gray-900 line-clamp-2">
                            {item.text.length > 100
                              ? `${item.text.substring(0, 100)}...`
                              : item.text}
                          </div>
                          <div className="text-xs text-gray-500">
                            Text Analysis
                          </div>
                        </div>
                      ) : (
                        <span className="text-sm text-gray-500">
                          No content
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        item.prediction === "Phishing"
                          ? "bg-red-100 text-red-800"
                          : "bg-green-100 text-green-800"
                      }`}
                    >
                      {item.prediction === "Phishing"
                        ? "⚠️ Phishing"
                        : "✅ Legitimate"}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          className={`h-2 rounded-full ${
                            item.prediction === "Phishing"
                              ? "bg-red-500"
                              : "bg-green-500"
                          }`}
                          style={{ width: `${item.confidence * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-900">
                        {Math.round(item.confidence * 100)}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full capitalize">
                      {item.model_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(item.timestamp)
                      .toISOString()
                      .replace("T", " ")
                      .slice(0, 19)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      {item.url && (
                        <button
                          onClick={() => {
                            if (typeof window !== "undefined")
                              window.open(item.url, "_blank");
                          }}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Visit
                        </button>
                      )}
                      <button
                        onClick={() => {
                          if (
                            typeof window !== "undefined" &&
                            navigator.clipboard
                          )
                            navigator.clipboard.writeText(
                              item.url || item.text || ""
                            );
                        }}
                        className="text-gray-600 hover:text-gray-900"
                      >
                        Copy
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {history.length === 0 && (
          <EmptyState
            title="No Predictions Found"
            description="No predictions match your current filters. Start analyzing URLs and text to see your prediction history here."
            icon="🔍"
            variant="hacker"
          />
        )}
      </div>
    </div>
  );
}
