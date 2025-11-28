import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { itemsService } from '../services/api';
import { MapPin, Calendar, User, Mail, Phone, ArrowLeft, Share2, CheckCircle } from 'lucide-react';
import { format } from 'date-fns';
import { useToast } from '../hooks/use-toast';
import { useAuth } from '../contexts/AuthContext';
import { claimsService } from '../services/api';
import ClaimModal from '../components/claims/ClaimModal';
import { ShieldCheck, AlertCircle } from 'lucide-react';

const ItemDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { toast } = useToast();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(0);
  const [isClaimModalOpen, setIsClaimModalOpen] = useState(false);
  const [userClaim, setUserClaim] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loadingMatches, setLoadingMatches] = useState(false);

  const fetchItemAndClaim = async () => {
    try {
      setLoading(true);
      const data = await itemsService.getById(id);
      // Transform API data to match component expectation
      const transformedItem = {
        ...data,
        category: data.category ? data.category.name : data.category_id, // Use name if available
        images: data.images && data.images.length > 0 ? data.images.map(img => img.image_url) : [],
        contactInfo: data.owner ? {
          name: data.owner.full_name || data.owner.username,
          email: data.owner.email,
          phone: data.owner.phone || 'Not provided'
        } : { name: 'Unknown', email: '', phone: '' },
        date: data.date_lost || data.created_at // Map date_lost to date
      };
      setItem(transformedItem);

      // Check if user has claimed this item
      if (user && data.type === 'found' && data.user_id !== user.id) {
        try {
          const myClaims = await claimsService.getMyClaims();
          const claim = myClaims.find(c => c.item_id === parseInt(id));
          setUserClaim(claim);
        } catch (err) {
          console.error("Failed to fetch claims", err);
        }
      }

    } catch (error) {
      console.error("Failed to fetch item:", error);
      toast({
        title: "Error",
        description: "Failed to load item details",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItemAndClaim();
    
    // Refresh when page becomes visible (user returns to tab)
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchItemAndClaim();
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [id, user]);

  // Fetch matches for lost items owned by current user
  useEffect(() => {
    if (item && user && item.type === 'lost' && item.user_id === user.id) {
      const fetchMatches = async () => {
        setLoadingMatches(true);
        try {
          const matchesData = await itemsService.getMatches(id);
          setMatches(matchesData);
        } catch (error) {
          console.error("Failed to fetch matches:", error);
        } finally {
          setLoadingMatches(false);
        }
      };
      fetchMatches();
    }
  }, [item, user, id]);

  const getTypeColor = (type) => {
    return type === 'lost'
      ? 'bg-red-100 text-red-700 border-red-200'
      : 'bg-green-100 text-green-700 border-green-200';
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

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: item.title,
        text: item.description,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      toast({
        title: 'Link copied!',
        description: 'Link copied to clipboard'
      });
    }
  };

  const handleContact = () => {
    toast({
      title: 'Contact Information',
      description: 'Contact details are shown below'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Loading item details...</p>
        </div>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Item Not Found</h2>
          <p className="text-gray-600 mb-4">The item you're looking for doesn't exist.</p>
          <Button onClick={() => navigate('/items')}>Browse Items</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-6">
        {/* Back Button */}
        <Button
          variant="outline"
          onClick={() => navigate('/items')}
          className="mb-3 sm:mb-4 text-sm"
          size="sm"
        >
          <ArrowLeft className="w-3 h-3 sm:w-4 sm:h-4 mr-1 sm:mr-2" />
          Back
        </Button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
          {/* Images */}
          <div>
            <Card className="p-3 sm:p-4 mb-3 sm:mb-4">
              <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden mb-4">
                {item.images && item.images.length > 0 ? (
                  <img
                    src={item.images[selectedImage]}
                    alt={item.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <MapPin className="w-16 h-16 text-gray-400" />
                  </div>
                )}
              </div>
              {item.images && item.images.length > 1 && (
                <div className="grid grid-cols-4 gap-2">
                  {item.images.map((img, index) => (
                    <button
                      key={index}
                      onClick={() => setSelectedImage(index)}
                      className={`aspect-square rounded-lg overflow-hidden border-2 ${selectedImage === index
                        ? 'border-blue-600'
                        : 'border-gray-200'
                        }`}
                    >
                      <img
                        src={img}
                        alt={`${item.title} ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </Card>
          </div>

          {/* Details */}
          <div>
            <Card className="p-4 sm:p-5">
              {/* Type and Category */}
              <div className="flex items-center gap-1.5 sm:gap-2 mb-3 sm:mb-4">
                <Badge className={`${getTypeColor(item.type)} font-semibold border text-xs`}>
                  {item.type === 'lost' ? 'LOST' : 'FOUND'}
                </Badge>
                <Badge variant="outline" className="text-xs">{getCategoryLabel(item.category)}</Badge>
                <Badge
                  variant="outline"
                  className="ml-auto bg-green-50 text-green-700 border-green-200 text-xs"
                >
                  {item.status.toUpperCase()}
                </Badge>
              </div>

              {/* Title */}
              <h1 className="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">{item.title}</h1>

              {/* Meta Info */}
              <div className="space-y-2 sm:space-y-2.5 mb-4 sm:mb-5">
                <div className="flex items-start">
                  <MapPin className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 mr-2 sm:mr-3 mt-0.5" />
                  <div>
                    <p className="text-xs sm:text-sm font-medium text-gray-700">Location</p>
                    <p className="text-sm sm:text-base text-gray-900">{item.location}</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <Calendar className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 mr-2 sm:mr-3 mt-0.5" />
                  <div>
                    <p className="text-xs sm:text-sm font-medium text-gray-700">Date</p>
                    <p className="text-sm sm:text-base text-gray-900">
                      {format(new Date(item.date), 'MMMM dd, yyyy - h:mm a')}
                    </p>
                  </div>
                </div>
              </div>

              {/* Description */}
              <div className="mb-4 sm:mb-5">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-1.5 sm:mb-2">Description</h3>
                <p className="text-sm sm:text-base text-gray-700 leading-relaxed">{item.description}</p>
              </div>

              {/* Contact Information */}
              <div className="border-t pt-4 sm:pt-5 mb-4 sm:mb-5">
                <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4">Contact Information</h3>
                <div className="space-y-2 sm:space-y-2.5">
                  <div className="flex items-center">
                    <User className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 mr-2 sm:mr-3" />
                    <div>
                      <p className="text-xs sm:text-sm font-medium text-gray-700">Name</p>
                      <p className="text-sm sm:text-base text-gray-900">{item.contactInfo.name}</p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Mail className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 mr-2 sm:mr-3" />
                    <div>
                      <p className="text-xs sm:text-sm font-medium text-gray-700">Email</p>
                      <a
                        href={`mailto:${item.contactInfo.email}`}
                        className="text-sm sm:text-base text-blue-600 hover:underline"
                      >
                        {item.contactInfo.email}
                      </a>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Phone className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600 mr-2 sm:mr-3" />
                    <div>
                      <p className="text-xs sm:text-sm font-medium text-gray-700">Phone</p>
                      <a
                        href={`tel:${item.contactInfo.phone}`}
                        className="text-sm sm:text-base text-blue-600 hover:underline"
                      >
                        {item.contactInfo.phone}
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                {/* For Lost Items - Show Contact Owner */}
                {item.type === 'lost' && (
                  <Button onClick={handleContact} className="flex-1">
                    <Mail className="w-4 h-4 mr-2" />
                    Contact Owner
                  </Button>
                )}

                {/* For Found Items - Show Claim This Item */}
                {item.type === 'found' && (
                  <>
                    {!user ? (
                      // Guest user - show claim button that redirects to login
                      <Button
                        onClick={() => navigate('/login', { state: { from: `/items/${id}`, action: 'claim' } })}
                        className="flex-1 bg-gray-900 hover:bg-black text-white text-sm sm:text-base shadow-lg"
                      >
                        Claim This Item
                      </Button>
                    ) : user.id === item.user_id ? (
                      // Owner viewing their own item
                      <p className="flex-1 text-xs sm:text-sm text-gray-500 italic py-3">This is your item</p>
                    ) : item.status === 'claimed' || (userClaim && userClaim.status === 'verified') ? (
                      // Item is claimed (by anyone) OR current user's claim is verified
                      <div className="flex-1 flex items-center gap-2 p-3 sm:p-4 bg-green-50 rounded-lg border border-green-200">
                        <CheckCircle className="w-4 h-4 sm:w-5 sm:h-5 text-green-600" />
                        <div>
                          <p className="text-sm sm:text-base font-medium text-green-900">Item Claimed</p>
                          <p className="text-xs sm:text-sm text-green-700">This item has been claimed</p>
                        </div>
                      </div>
                    ) : (
                      // User can claim (no claim OR pending/rejected claim)
                      <Button
                        onClick={() => setIsClaimModalOpen(true)}
                        className="flex-1 bg-gray-900 hover:bg-black text-white text-sm sm:text-base shadow-lg"
                      >
                        Claim This Item
                      </Button>
                    )}
                  </>
                )}

                {/* Share Button - always visible on the right */}
                <Button variant="outline" onClick={handleShare}>
                  <Share2 className="w-4 h-4 mr-2" />
                  Share
                </Button>
              </div>

              {/* Claim Status Info (if user has pending/rejected claim) */}
              {item.type === 'found' && user && userClaim && userClaim.status !== 'verified' && (
                <div className="mt-3 flex flex-col gap-2">
                  <div className="flex items-center justify-between p-3 sm:p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 sm:w-5 sm:h-5 text-blue-600" />
                      <div>
                        <p className="text-sm sm:text-base font-medium text-blue-900">Claim Submitted</p>
                        <p className="text-xs sm:text-sm text-blue-700">
                          Status: <span className="font-semibold">{userClaim.status}</span>
                        </p>
                      </div>
                    </div>
                  </div>
                  <Button
                    onClick={() => navigate('/my-claims')}
                    variant="outline"
                    className="w-full text-sm sm:text-base"
                  >
                    View My Claims
                  </Button>
                </div>
              )}

              <ClaimModal
                isOpen={isClaimModalOpen}
                onClose={() => setIsClaimModalOpen(false)}
                itemId={item.id}
                itemTitle={item.title}
                onSuccess={() => {
                  // Refresh item and claim status
                  fetchItemAndClaim();
                }}
              />
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItemDetailPage;
