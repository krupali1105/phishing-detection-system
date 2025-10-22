"use client";

import React from 'react';

interface ModernLoaderProps {
  text?: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'spinner' | 'dots' | 'pulse' | 'wave';
}

export default function ModernLoader({ 
  text = 'Loading...', 
  size = 'md',
  variant = 'spinner'
}: ModernLoaderProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  if (variant === 'dots') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        <div className="flex space-x-1">
          {[...Array(3)].map((_, i) => (
            <div 
              key={i}
              className={`${sizeClasses[size]} bg-blue-500 rounded-full animate-bounce`}
              style={{ animationDelay: `${i * 0.1}s` }}
            ></div>
          ))}
        </div>
        <div className={`${textSizeClasses[size]} text-gray-600 font-medium`}>
          {text}
        </div>
      </div>
    );
  }

  if (variant === 'pulse') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        <div className={`${sizeClasses[size]} bg-gradient-to-r from-blue-500 to-purple-600 rounded-full animate-pulse`}></div>
        <div className={`${textSizeClasses[size]} text-gray-600 font-medium`}>
          {text}
        </div>
      </div>
    );
  }

  if (variant === 'wave') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        <div className="flex space-x-1">
          {[...Array(5)].map((_, i) => (
            <div 
              key={i}
              className="w-1 h-6 bg-blue-500 rounded-full animate-pulse"
              style={{ 
                animationDelay: `${i * 0.1}s`,
                animationDuration: '1.2s'
              }}
            ></div>
          ))}
        </div>
        <div className={`${textSizeClasses[size]} text-blue-600 font-medium`}>
          {text}
        </div>
      </div>
    );
  }

  // Default spinner
  return (
    <div className="flex flex-col items-center justify-center space-y-3">
      <div className={`${sizeClasses[size]} border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin`}></div>
      <div className={`${textSizeClasses[size]} text-gray-600 font-medium`}>
        {text}
      </div>
    </div>
  );
}
