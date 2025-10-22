import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  variant?: 'default' | 'hacker' | 'dots' | 'pulse' | 'wave' | 'orbit';
}

export default function LoadingSpinner({ 
  size = 'md', 
  text = 'Loading...', 
  variant = 'hacker' 
}: LoadingSpinnerProps) {
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

  if (variant === 'hacker') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        {/* Enhanced hacker spinner */}
        <div className="relative">
          <div className={`${sizeClasses[size]} border-2 border-green-400 rounded-full animate-spin`}>
            <div className="absolute inset-0 border-2 border-transparent border-t-green-400 rounded-full animate-pulse"></div>
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-ping"></div>
          </div>
          {/* Scanning lines */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-full h-0.5 bg-green-400/50 animate-pulse"></div>
          </div>
        </div>
        
        {/* Enhanced text effect */}
        <div className="text-green-400 font-mono text-center">
          <div className={`${textSizeClasses[size]} font-medium`}>
            {text.split('').map((char, index) => (
              <span 
                key={index}
                className="inline-block animate-pulse"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {char === ' ' ? '\u00A0' : char}
              </span>
            ))}
          </div>
        </div>
        
        {/* Enhanced dots */}
        <div className="flex space-x-1">
          {[...Array(4)].map((_, i) => (
            <div 
              key={i}
              className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"
              style={{ animationDelay: `${i * 0.15}s` }}
            ></div>
          ))}
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
        <div className={`${textSizeClasses[size]} text-blue-600 font-medium animate-pulse`}>
          {text}
        </div>
      </div>
    );
  }

  if (variant === 'orbit') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        <div className="relative">
          <div className={`${sizeClasses[size]} border-2 border-purple-400 rounded-full animate-spin`}>
            <div className="absolute -top-1 -left-1 w-2 h-2 bg-purple-400 rounded-full"></div>
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-1 h-1 bg-purple-400 rounded-full animate-ping"></div>
          </div>
        </div>
        <div className={`${textSizeClasses[size]} text-purple-600 font-medium animate-pulse`}>
          {text}
        </div>
      </div>
    );
  }

  if (variant === 'dots') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        <div className="flex space-x-1">
          {[...Array(3)].map((_, i) => (
            <div 
              key={i}
              className={`${sizeClasses[size].split(' ')[0]} ${sizeClasses[size].split(' ')[1]} bg-blue-500 rounded-full animate-bounce`}
              style={{ animationDelay: `${i * 0.1}s` }}
            ></div>
          ))}
        </div>
        <div className={`${textSizeClasses[size]} text-gray-600 animate-pulse`}>
          {text}
        </div>
      </div>
    );
  }

  if (variant === 'pulse') {
    return (
      <div className="flex flex-col items-center justify-center space-y-3">
        <div className={`${sizeClasses[size]} bg-gradient-to-r from-blue-500 to-purple-600 rounded-full animate-pulse`}></div>
        <div className={`${textSizeClasses[size]} text-gray-600 animate-pulse`}>
          {text}
        </div>
      </div>
    );
  }

  // Default spinner
  return (
    <div className="flex flex-col items-center justify-center space-y-3">
      <div className={`${sizeClasses[size]} border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin`}></div>
      <div className={`${textSizeClasses[size]} text-gray-600 animate-pulse`}>
        {text}
      </div>
    </div>
  );
}
