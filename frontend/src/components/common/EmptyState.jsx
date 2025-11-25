import React from 'react';
import { Button } from '../ui/button';
import { Package, Search, PlusCircle } from 'lucide-react';

const EmptyState = ({
    icon: Icon = Package,
    title = "No items found",
    description = "There are no items to display at the moment.",
    actionLabel,
    onAction,
    secondaryActionLabel,
    onSecondaryAction
}) => {
    return (
        <div className="flex flex-col items-center justify-center py-16 px-4">
            <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
                <Icon className="w-12 h-12 text-gray-400" />
            </div>

            <h3 className="text-xl font-semibold text-gray-900 mb-2 text-center">
                {title}
            </h3>

            <p className="text-gray-600 mb-6 text-center max-w-md">
                {description}
            </p>

            <div className="flex flex-col sm:flex-row gap-3">
                {actionLabel && onAction && (
                    <Button onClick={onAction} size="lg">
                        <PlusCircle className="w-4 h-4 mr-2" />
                        {actionLabel}
                    </Button>
                )}

                {secondaryActionLabel && onSecondaryAction && (
                    <Button onClick={onSecondaryAction} variant="outline" size="lg">
                        <Search className="w-4 h-4 mr-2" />
                        {secondaryActionLabel}
                    </Button>
                )}
            </div>
        </div>
    );
};

export default EmptyState;
