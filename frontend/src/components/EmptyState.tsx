import React from 'react';

interface EmptyStateProps {
  title: string;
  description: string;
  icon?: string;
  variant?: 'default' | 'hacker' | 'warning' | 'success';
}

export default function EmptyState({ 
  title, 
  description, 
  icon = "📊",
  variant = 'default' 
}: EmptyStateProps) {
  const variantStyles = {
    default: {
      container: 'bg-gray-50 border-gray-200',
      icon: 'text-gray-400',
      title: 'text-gray-900',
      description: 'text-gray-600'
    },
    hacker: {
      container: 'bg-green-50 border-green-200',
      icon: 'text-green-400',
      title: 'text-green-900 font-mono',
      description: 'text-green-700 font-mono'
    },
    warning: {
      container: 'bg-yellow-50 border-yellow-200',
      icon: 'text-yellow-400',
      title: 'text-yellow-900',
      description: 'text-yellow-700'
    },
    success: {
      container: 'bg-green-50 border-green-200',
      icon: 'text-green-400',
      title: 'text-green-900',
      description: 'text-green-700'
    }
  };

  const styles = variantStyles[variant];

  return (
    <div className={`flex flex-col items-center justify-center p-12 border-2 border-dashed rounded-lg ${styles.container}`}>
      {/* Animated icon */}
      <div className={`text-6xl mb-4 ${styles.icon} ${variant === 'hacker' ? 'animate-pulse' : ''}`}>
        {variant === 'hacker' ? (
          <div className="relative">
            <div className="animate-spin">⚡</div>
            <div className="absolute inset-0 animate-ping opacity-20">🔒</div>
          </div>
        ) : (
          icon
        )}
      </div>

      {/* Title */}
      <h3 className={`text-xl font-semibold mb-2 ${styles.title}`}>
        {variant === 'hacker' ? (
          <span className="font-mono">
            {title.split('').map((char, index) => (
              <span 
                key={index}
                className="inline-block animate-pulse"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {char === ' ' ? '\u00A0' : char}
              </span>
            ))}
          </span>
        ) : (
          title
        )}
      </h3>

      {/* Description */}
      <p className={`text-center max-w-md ${styles.description}`}>
        {variant === 'hacker' ? (
          <span className="font-mono text-sm">
            {description}
          </span>
        ) : (
          description
        )}
      </p>

      {/* Hacker-style dots */}
      {variant === 'hacker' && (
        <div className="flex space-x-1 mt-4">
          {[...Array(3)].map((_, i) => (
            <div 
              key={i}
              className="w-2 h-2 bg-green-400 rounded-full animate-pulse"
              style={{ animationDelay: `${i * 0.2}s` }}
            ></div>
          ))}
        </div>
      )}
    </div>
  );
}
