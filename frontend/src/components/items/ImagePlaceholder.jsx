import React from 'react';
import {
    Smartphone,
    Wallet,
    Key,
    ShoppingBag,
    Diamond,
    FileText,
    Dog,
    Package
} from 'lucide-react';

const getCategoryIcon = (category) => {
    const iconMap = {
        electronics: Smartphone,
        wallet: Wallet,
        keys: Key,
        bag: ShoppingBag,
        jewelry: Diamond,
        documents: FileText,
        pets: Dog,
        other: Package
    };

    return iconMap[category?.toLowerCase()] || Package;
};

const ImagePlaceholder = ({ category }) => {
    const Icon = getCategoryIcon(category);

    const gradients = {
        electronics: 'from-blue-100 to-blue-200',
        wallet: 'from-green-100 to-green-200',
        keys: 'from-yellow-100 to-yellow-200',
        bag: 'from-purple-100 to-purple-200',
        jewelry: 'from-pink-100 to-pink-200',
        documents: 'from-orange-100 to-orange-200',
        pets: 'from-red-100 to-red-200',
        other: 'from-gray-100 to-gray-200'
    };

    const gradient = gradients[category?.toLowerCase()] || gradients.other;

    return (
        <div className={`w-full h-full flex items-center justify-center bg-gradient-to-br ${gradient}`}>
            <Icon className="w-16 h-16 text-gray-400" strokeWidth={1.5} />
        </div>
    );
};

export default ImagePlaceholder;
