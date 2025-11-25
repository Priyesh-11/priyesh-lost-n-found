import React from 'react';
import { Search } from 'lucide-react';

const PageLoader = () => {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-white">
            {/* Loader Container */}
            <div className="relative flex flex-col items-center justify-center px-4">
                {/* Magnifying Glass Icon - Smaller */}
                <div className="relative w-12 h-12 sm:w-16 sm:h-16 flex items-center justify-center">
                    {/* Outer Rings */}
                    <div className="absolute inset-0 rounded-full border-2 border-blue-100 animate-ping" />
                    <div className="absolute inset-0 rounded-full border-2 border-blue-500 border-t-transparent animate-spin"
                        style={{ animationDuration: '1s' }} />

                    {/* Magnifying Glass */}
                    <div className="relative">
                        <Search
                            className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600"
                            strokeWidth={2.5}
                        />
                    </div>
                </div>

                {/* Loading Text */}
                <div className="mt-4 text-center">
                    <h2 className="text-sm font-medium text-gray-600 animate-pulse">
                        Loading...
                    </h2>
                </div>
            </div>
        </div>
    );
};

export default PageLoader;
