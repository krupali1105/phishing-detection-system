"use client";

import React, { useState, useEffect } from "react";
import ModernLoader from "./ModernLoader";

interface AnalyticsData {
  total_predictions: number;
  phishing_count: number;
  legitimate_count: number;
  phishing_percentage: number;
  avg_confidence: number;
  model_usage: {
    url: number;
    text: number;
    hybrid: number;
  };
}

interface DailyStats {
  date: string;
  total_predictions: number;
  phishing_count: number;
  legitimate_count: number;
  avg_confidence: number;
}

interface ModelPerformance {
  [key: string]: {
    total_predictions: number;
    phishing_count: number;
    legitimate_count: number;
    phishing_percentage: number;
    avg_confidence: number;
  };
}

export default function AnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [dailyStats, setDailyStats] = useState<DailyStats[]>([]);
  const [modelPerformance, setModelPerformance] = useState<ModelPerformance>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      
      // Fetch analytics summary
      const summaryResponse = await fetch("http://localhost:8000/analytics/summary");
      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json();
        setAnalytics(summaryData);
      }

      // Fetch daily stats
      const dailyResponse = await fetch("http://localhost:8000/analytics/daily-stats?days=7");
      if (dailyResponse.ok) {
        const dailyData = await dailyResponse.json();
        setDailyStats(dailyData);
      }

      // Fetch model performance
      const performanceResponse = await fetch("http://localhost:8000/analytics/model-performance");
      if (performanceResponse.ok) {
        const performanceData = await performanceResponse.json();
        setModelPerformance(performanceData);
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch analytics");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <ModernLoader size="lg" text="Loading Analytics..." variant="spinner" />
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
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
        <p className="text-gray-600">Comprehensive insights into phishing detection performance</p>
      </div>

      {/* Summary Cards */}
      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Predictions</p>
                <p className="text-2xl font-bold text-gray-900">{analytics.total_predictions}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Phishing Detected</p>
                <p className="text-2xl font-bold text-red-600">{analytics.phishing_count}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Legitimate</p>
                <p className="text-2xl font-bold text-green-600">{analytics.legitimate_count}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Avg Confidence</p>
                <p className="text-2xl font-bold text-purple-600">{Math.round(analytics.avg_confidence * 100)}%</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Phishing vs Legitimate Chart */}
        {analytics && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Detection Distribution</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-red-500 rounded mr-2"></div>
                  <span className="text-sm font-medium text-gray-700">Phishing</span>
                </div>
                <span className="text-sm font-bold text-gray-900">{analytics.phishing_percentage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-red-500 h-3 rounded-full"
                  style={{ width: `${analytics.phishing_percentage}%` }}
                ></div>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-4 h-4 bg-green-500 rounded mr-2"></div>
                  <span className="text-sm font-medium text-gray-700">Legitimate</span>
                </div>
                <span className="text-sm font-bold text-gray-900">{(100 - analytics.phishing_percentage).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-green-500 h-3 rounded-full"
                  style={{ width: `${100 - analytics.phishing_percentage}%` }}
                ></div>
              </div>
            </div>
          </div>
        )}

        {/* Model Usage Chart */}
        {analytics && (
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Model Usage</h3>
            <div className="space-y-4">
              {Object.entries(analytics.model_usage).map(([model, count]) => (
                <div key={model} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 capitalize">{model}</span>
                    <span className="text-sm font-bold text-gray-900">{count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{ 
                        width: `${analytics.total_predictions > 0 ? (count / analytics.total_predictions) * 100 : 0}%` 
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Model Performance Table */}
      {Object.keys(modelPerformance).length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Model Performance</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Model</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phishing</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Legitimate</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phishing %</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Confidence</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(modelPerformance).map(([model, performance]) => (
                  <tr key={model}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 capitalize">{model}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{performance.total_predictions}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">{performance.phishing_count}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">{performance.legitimate_count}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{performance.phishing_percentage.toFixed(1)}%</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{Math.round(performance.avg_confidence * 100)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Daily Stats Chart */}
      {dailyStats.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Daily Statistics (Last 7 Days)</h3>
          <div className="space-y-4">
            {dailyStats.map((day, index) => (
              <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">{day.date}</span>
                  <span className="text-sm font-bold text-gray-900">{day.total_predictions} predictions</span>
                </div>
                <div className="flex space-x-4 text-xs">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-red-500 rounded mr-1"></div>
                    <span className="text-red-600">{day.phishing_count} phishing</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-green-500 rounded mr-1"></div>
                    <span className="text-green-600">{day.legitimate_count} legitimate</span>
                  </div>
                  <div className="text-gray-500">
                    Avg confidence: {Math.round(day.avg_confidence * 100)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
