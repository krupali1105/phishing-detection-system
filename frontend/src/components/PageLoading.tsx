"use client";

import React from 'react';
import ModernLoader from './ModernLoader';

interface PageLoadingProps {
  isVisible: boolean;
  message?: string;
}

export default function PageLoading({ 
  isVisible, 
  message = "Processing..."
}: PageLoadingProps) {
  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-white/10 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100 max-w-sm w-full mx-4">
        <div className="text-center">
          <ModernLoader 
            text={message}
            size="lg"
            variant="spinner"
          />
        </div>
      </div>
    </div>
  );
}
