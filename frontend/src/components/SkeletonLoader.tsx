import React from 'react';

interface SkeletonLoaderProps {
  variant?: 'card' | 'table' | 'chart' | 'list';
  count?: number;
  className?: string;
}

export default function SkeletonLoader({ 
  variant = 'card', 
  count = 1,
  className = ''
}: SkeletonLoaderProps) {
  const renderCardSkeleton = () => (
    <div className="bg-white p-6 rounded-lg shadow animate-pulse">
      <div className="flex items-center space-x-4 mb-4">
        <div className="w-12 h-12 bg-gray-300 rounded-full"></div>
        <div className="space-y-2 flex-1">
          <div className="h-4 bg-gray-300 rounded w-3/4"></div>
          <div className="h-3 bg-gray-300 rounded w-1/2"></div>
        </div>
      </div>
      <div className="space-y-3">
        <div className="h-4 bg-gray-300 rounded"></div>
        <div className="h-4 bg-gray-300 rounded w-5/6"></div>
        <div className="h-4 bg-gray-300 rounded w-4/6"></div>
      </div>
    </div>
  );

  const renderTableSkeleton = () => (
    <div className="bg-white rounded-lg shadow animate-pulse">
      <div className="p-6">
        <div className="h-6 bg-gray-300 rounded w-1/4 mb-4"></div>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex space-x-4">
              <div className="h-4 bg-gray-300 rounded flex-1"></div>
              <div className="h-4 bg-gray-300 rounded w-20"></div>
              <div className="h-4 bg-gray-300 rounded w-16"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderChartSkeleton = () => (
    <div className="bg-white p-6 rounded-lg shadow animate-pulse">
      <div className="h-6 bg-gray-300 rounded w-1/3 mb-6"></div>
      <div className="h-64 bg-gray-300 rounded"></div>
      <div className="flex justify-between mt-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="text-center">
            <div className="h-4 bg-gray-300 rounded w-16 mb-2"></div>
            <div className="h-3 bg-gray-300 rounded w-12"></div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderListSkeleton = () => (
    <div className="space-y-3">
      {[...Array(count)].map((_, i) => (
        <div key={i} className="flex items-center space-x-3 p-3 bg-gray-50 rounded animate-pulse">
          <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
          <div className="flex-1 space-y-2">
            <div className="h-4 bg-gray-300 rounded w-3/4"></div>
            <div className="h-3 bg-gray-300 rounded w-1/2"></div>
          </div>
          <div className="w-16 h-6 bg-gray-300 rounded"></div>
        </div>
      ))}
    </div>
  );

  const renderSkeleton = () => {
    switch (variant) {
      case 'table':
        return renderTableSkeleton();
      case 'chart':
        return renderChartSkeleton();
      case 'list':
        return renderListSkeleton();
      default:
        return renderCardSkeleton();
    }
  };

  return (
    <div className={className}>
      {variant === 'list' ? (
        renderSkeleton()
      ) : (
        <div className="grid gap-4">
          {[...Array(count)].map((_, i) => (
            <div key={i}>
              {renderSkeleton()}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
