import React from 'react';
import { Card } from '../ui/card';

const ItemCardSkeleton = () => {
    return (
        <Card className="overflow-hidden">
            {/* Image Skeleton */}
            <div className="relative h-48 bg-gray-200 animate-pulse" />

            {/* Content Skeleton */}
            <div className="p-4 space-y-3">
                {/* Category Badge Skeleton */}
                <div className="h-5 w-20 bg-gray-200 rounded animate-pulse" />

                {/* Title Skeleton */}
                <div className="h-6 bg-gray-200 rounded animate-pulse w-3/4" />

                {/* Description Skeleton */}
                <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-full" />
                    <div className="h-4 bg-gray-200 rounded animate-pulse w-2/3" />
                </div>

                {/* Meta Info Skeleton */}
                <div className="space-y-2 pt-2">
                    <div className="h-3 bg-gray-200 rounded animate-pulse w-1/2" />
                    <div className="h-3 bg-gray-200 rounded animate-pulse w-1/3" />
                </div>
            </div>
        </Card>
    );
};

export default ItemCardSkeleton;
