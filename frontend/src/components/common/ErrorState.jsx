import React from 'react';
import { Button } from '../ui/button';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { Alert, AlertDescription } from '../ui/alert';

const ErrorState = ({
    title = "Something went wrong",
    message = "We encountered an error while loading this content.",
    onRetry,
    showRetry = true
}) => {
    return (
        <div className="flex flex-col items-center justify-center py-16 px-4">
            <div className="w-24 h-24 bg-red-50 rounded-full flex items-center justify-center mb-6">
                <AlertCircle className="w-12 h-12 text-red-500" />
            </div>

            <h3 className="text-xl font-semibold text-gray-900 mb-2 text-center">
                {title}
            </h3>

            <p className="text-gray-600 mb-6 text-center max-w-md">
                {message}
            </p>

            {showRetry && onRetry && (
                <Button onClick={onRetry} variant="outline" size="lg">
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Try Again
                </Button>
            )}

            <Alert variant="destructive" className="mt-6 max-w-md">
                <AlertDescription className="text-sm">
                    If this problem persists, please contact support or try again later.
                </AlertDescription>
            </Alert>
        </div>
    );
};

export default ErrorState;
