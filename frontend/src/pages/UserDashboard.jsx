import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Badge } from '../components/ui/badge';
import ItemCard from '../components/items/ItemCard';
import EmptyState from '../components/common/EmptyState';
import { itemsService, claimsService } from '../services/api';
import { Package, TrendingUp, Plus, ArrowRight, Award } from 'lucide-react';

const UserDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [userItems, setUserItems] = useState([]);
  const [userClaims, setUserClaims] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    lost: 0,
    found: 0,
    resolved: 0,
    claims: 0
  });

  const fetchUserData = async () => {
    if (!user?.id) return;

    try {
      const data = await itemsService.getAll({ user_id: user.id, status: 'all' });
      const items = Array.isArray(data) ? data : data.items || [];

      const mappedItems = items.map(item => ({
        ...item,
        category: item.category ? item.category.name : 'other',
        images: item.images && item.images.length > 0 ? item.images.map(img => img.image_url) : []
      }));

      setUserItems(mappedItems);

      const claimsData = await claimsService.getMyClaims();
      setUserClaims(claimsData);

      const lostItems = mappedItems.filter(i => i.type === 'lost');
      const foundItems = mappedItems.filter(i => i.type === 'found');
      const resolvedItems = mappedItems.filter(i => i.status === 'resolved');

      setStats({
        total: mappedItems.length,
        lost: lostItems.length,
        found: foundItems.length,
        resolved: resolvedItems.length,
        claims: claimsData.length
      });
    } catch (error) {
      console.error("Failed to fetch user data:", error);
    }
  };

  useEffect(() => {
    fetchUserData();
    
    // Refresh when page becomes visible (user returns to tab)
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchUserData();
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [user]);

  const lostItems = userItems.filter(i => i.type === 'lost');
  const foundItems = userItems.filter(i => i.type === 'found');

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 md:py-12">

        {/* Header Section - Responsive */}
        <div className="mb-6 sm:mb-8 md:mb-12">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Dashboard</h1>
              <p className="text-sm sm:text-base text-gray-600 mt-1">Welcome back, {user?.full_name || user?.username}</p>
            </div>

            {/* Reputation Badge - Compact on Mobile */}
            <div className="flex items-center gap-2 sm:gap-3 bg-white rounded-xl sm:rounded-2xl px-4 sm:px-6 py-2 sm:py-3 shadow-sm border border-gray-100 self-start sm:self-auto">
              <Award className="w-4 h-4 sm:w-5 sm:h-5 text-yellow-500" />
              <div className="text-right">
                <div className="text-xl sm:text-2xl font-bold text-gray-900">{user?.reputation_score || 0}</div>
                <div className="text-xs text-gray-500">Reputation</div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Grid - Compact on Mobile */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8 md:mb-12">
          <StatCard value={stats.total} label="Total Items" color="blue" />
          <StatCard value={stats.lost} label="Lost" color="red" />
          <StatCard value={stats.found} label="Found" color="green" />
          <StatCard value={stats.claims} label="Claims" color="orange" />
        </div>

        {/* Quick Actions - Stack on Mobile */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-6 sm:mb-8 md:mb-12">
          <ActionButton
            onClick={() => navigate('/report-lost')}
            icon={<Plus className="w-5 h-5" />}
            title="Report Lost Item"
            description="Lost something? Let the community help you find it"
            color="red"
          />
          <ActionButton
            onClick={() => navigate('/report-found')}
            icon={<Plus className="w-5 h-5" />}
            title="Report Found Item"
            description="Found something? Help someone get it back"
            color="green"
          />
        </div>

        {/* Content Tabs - Responsive */}
        <Tabs defaultValue="all" className="w-full">
          <TabsList className="bg-white border border-gray-200 p-1 rounded-xl shadow-sm inline-flex w-auto">
            <TabsTrigger value="all" className="rounded-lg text-xs sm:text-sm whitespace-nowrap px-4">All ({stats.total})</TabsTrigger>
            <TabsTrigger value="lost" className="rounded-lg text-xs sm:text-sm whitespace-nowrap px-4">Lost ({stats.lost})</TabsTrigger>
            <TabsTrigger value="found" className="rounded-lg text-xs sm:text-sm whitespace-nowrap px-4">Found ({stats.found})</TabsTrigger>
            <TabsTrigger value="claims" className="rounded-lg text-xs sm:text-sm whitespace-nowrap px-4">Claims ({stats.claims})</TabsTrigger>
          </TabsList>

          {/* All Items */}
          <TabsContent value="all" className="mt-6 sm:mt-8">
            {userItems.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5 md:gap-6">
                {userItems.map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Package}
                title="No items yet"
                description="You haven't reported any items yet. Get started by reporting a lost or found item."
                actionLabel="Report Item"
                onAction={() => navigate('/report-lost')}
              />
            )}
          </TabsContent>

          {/* Lost Items */}
          <TabsContent value="lost" className="mt-6 sm:mt-8">
            {lostItems.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5 md:gap-6">
                {lostItems.map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Package}
                title="No lost items"
                description="You haven't reported any lost items."
                actionLabel="Report Lost Item"
                onAction={() => navigate('/report-lost')}
              />
            )}
          </TabsContent>

          {/* Found Items */}
          <TabsContent value="found" className="mt-6 sm:mt-8">
            {foundItems.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5 md:gap-6">
                {foundItems.map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Package}
                title="No found items"
                description="You haven't reported any found items."
                actionLabel="Report Found Item"
                onAction={() => navigate('/report-found')}
              />
            )}
          </TabsContent>

          {/* My Claims */}
          <TabsContent value="claims" className="mt-6 sm:mt-8">
            {userClaims.length > 0 ? (
              <div className="space-y-3 sm:space-y-4">
                {userClaims.map((claim) => (
                  <ClaimCard key={claim.id} claim={claim} navigate={navigate} />
                ))}
              </div>
            ) : (
              <EmptyState
                icon={Package}
                title="No claims yet"
                description="You haven't submitted any claims yet."
                actionLabel="Browse Items"
                onAction={() => navigate('/items')}
              />
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

// Compact Stat Card for Mobile
const StatCard = ({ value, label, color }) => {
  const colors = {
    blue: 'border-blue-200 bg-blue-50/50',
    red: 'border-red-200 bg-red-50/50',
    green: 'border-green-200 bg-green-50/50',
    orange: 'border-orange-200 bg-orange-50/50'
  };

  const textColors = {
    blue: 'text-blue-600',
    red: 'text-red-600',
    green: 'text-green-600',
    orange: 'text-orange-600'
  };

  return (
    <div className={`${colors[color]} border rounded-xl sm:rounded-2xl p-3 sm:p-4 md:p-6 transition-all hover:shadow-md`}>
      <div className={`text-2xl sm:text-3xl md:text-4xl font-bold ${textColors[color]} mb-0.5 sm:mb-1`}>{value}</div>
      <div className="text-xs sm:text-sm text-gray-600 font-medium">{label}</div>
    </div>
  );
};

// Compact Action Button for Mobile
const ActionButton = ({ onClick, icon, title, description, color }) => {
  const colors = {
    red: 'hover:bg-red-50 hover:border-red-200 group-hover:text-red-600',
    green: 'hover:bg-green-50 hover:border-green-200 group-hover:text-green-600'
  };

  return (
    <button
      onClick={onClick}
      className={`group bg-white border border-gray-200 rounded-xl sm:rounded-2xl p-4 sm:p-5 md:p-6 text-left transition-all hover:shadow-md ${colors[color]}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3 sm:gap-4 flex-1 min-w-0">
          <div className="p-2 sm:p-3 bg-gray-50 rounded-lg sm:rounded-xl group-hover:bg-white transition-colors flex-shrink-0">
            {icon}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-sm sm:text-base md:text-lg font-semibold text-gray-900 mb-0.5 sm:mb-1 truncate">{title}</h3>
            <p className="text-xs sm:text-sm text-gray-600 line-clamp-1 sm:line-clamp-2">{description}</p>
          </div>
        </div>
        <ArrowRight className="w-4 h-4 sm:w-5 sm:h-5 text-gray-400 group-hover:translate-x-1 transition-transform flex-shrink-0 mt-1" />
      </div>
    </button>
  );
};

// Minimalist Claim Card
const ClaimCard = ({ claim, navigate }) => {
  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-700',
    verified: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700'
  };

  return (
    <div className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-md transition-all">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-3">
            <h3 className="text-lg font-semibold text-gray-900">{claim.item_title || 'Item'}</h3>
            <Badge className={`${statusColors[claim.status]} border-0`}>
              {claim.status}
            </Badge>
          </div>
          <p className="text-sm text-gray-600 mb-4 line-clamp-2">{claim.proof_description}</p>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate(`/items/${claim.item_id}`)}
            className="rounded-lg"
          >
            View Item
          </Button>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;