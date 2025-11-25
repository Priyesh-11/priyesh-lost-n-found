import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { MapPin, Calendar, Tag } from 'lucide-react';
import ImagePlaceholder from './ImagePlaceholder';
import { formatRelativeTime, getStatusColor, getStatusLabel } from '../../utils/formatters';

const ItemCard = ({ item }) => {
  const navigate = useNavigate();

  const getTypeColor = (type) => {
    return type === 'lost' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700';
  };

  const getCategoryLabel = (category) => {
    const labels = {
      electronics: 'Electronics',
      wallet: 'Wallet',
      keys: 'Keys',
      bag: 'Bag',
      jewelry: 'Jewelry',
      documents: 'Documents',
      pets: 'Pets',
      other: 'Other'
    };
    return labels[category] || category;
  };

  const handleClick = () => {
    navigate(`/items/${item.id}`);
  };

  return (
    <Card
      className="overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer group border-2 border-transparent hover:border-blue-200"
      onClick={handleClick}
    >
      {/* Image */}
      <div className="relative h-36 sm:h-44 md:h-48 overflow-hidden bg-gray-100">
        {item.images && item.images.length > 0 ? (
          <img
            src={item.images[0]}
            alt={item.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        ) : (
          <ImagePlaceholder category={item.category} />
        )}

        {/* Badges Container - Top Right */}
        <div className="absolute top-2 right-2 sm:top-3 sm:right-3 flex flex-col gap-1.5 sm:gap-2">
          {/* Type Badge */}
          <Badge className={`${getTypeColor(item.type)} font-semibold border shadow-sm text-xs`}>
            {item.type === 'lost' ? 'LOST' : 'FOUND'}
          </Badge>

          {/* Status Badge (only if not active) */}
          {item.status && item.status !== 'active' && (
            <Badge className={`${getStatusColor(item.status)} font-semibold border shadow-sm text-xs`}>
              {getStatusLabel(item.status)}
            </Badge>
          )}

          {/* Claims Badge */}
          {item.claims_count > 0 && (
            <Badge className="bg-orange-100 text-orange-700 border-orange-200 shadow-sm animate-pulse text-xs">
              {item.claims_count} {item.claims_count === 1 ? 'Claim' : 'Claims'}
            </Badge>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="p-3 sm:p-4">
        {/* Category */}
        <div className="mb-2">
          <Badge variant="outline" className="text-xs">
            {getCategoryLabel(item.category)}
          </Badge>
        </div>

        {/* Title */}
        <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-2 line-clamp-1 group-hover:text-blue-600 transition-colors">
          {item.title}
        </h3>

        {/* Description */}
        <p className="text-sm text-gray-600 mb-3 sm:mb-4 line-clamp-2">
          {item.description}
        </p>

        {/* Meta Info */}
        <div className="space-y-1.5 sm:space-y-2">
          <div className="flex items-center text-xs text-gray-500">
            <MapPin className="w-4 h-4 mr-1.5 text-blue-600 flex-shrink-0" />
            <span className="line-clamp-1">{item.location}</span>
          </div>
          <div className="flex items-center text-xs text-gray-500">
            <Calendar className="w-4 h-4 mr-1.5 text-blue-600 flex-shrink-0" />
            <span>{formatRelativeTime(item.date)}</span>
          </div>
        </div>
      </div>

      {/* Hover Overlay Effect */}
      <div className="absolute inset-0 bg-blue-500/0 group-hover:bg-blue-500/5 transition-all duration-300 pointer-events-none" />
    </Card>
  );
};

export default ItemCard;