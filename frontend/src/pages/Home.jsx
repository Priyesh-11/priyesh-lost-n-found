import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import ItemCard from '../components/items/ItemCard';
import ItemCardSkeleton from '../components/items/ItemCardSkeleton';
import EmptyState from '../components/common/EmptyState';
import ErrorState from '../components/common/ErrorState';
import { itemsService } from '../services/api';
import LightRays from '../components/ui/LightRays';
import Shuffle from '../components/ui/shuffle-text';
import {
  Camera, BrainCircuit, ShieldCheck, Bell, ArrowRight,
  CheckCircle, Users, Shield
} from 'lucide-react';

const Home = () => {
  const navigate = useNavigate();
  const [latestItems, setLatestItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await itemsService.getAll({
        status: 'active',
        sort: 'desc',
        limit: 4
      });
      const items = Array.isArray(data) ? data : data.items || [];

      const mappedItems = items.map(item => ({
        ...item,
        category: item.category ? item.category.name : 'other',
        images: item.images && item.images.length > 0 ? item.images.map(img => img.image_url) : [],
        date: item.date_lost || item.date_found || item.created_at
      }));

      setLatestItems(mappedItems);
    } catch (error) {
      console.error('Failed to fetch items:', error);
      setError(error.message || 'Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
    
    // Refresh items when page becomes visible (user returns to tab)
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchItems();
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  return (
    <div className="bg-white overflow-x-hidden">

      {/* SECTION 1: Hero */}
      <section className="min-h-screen w-full flex items-center justify-center relative bg-gradient-to-br from-black via-gray-900 to-black py-12 sm:py-16 md:py-20 overflow-hidden">
        {/* LightRays Background */}
        <div className="absolute inset-0 w-full h-full opacity-100 z-10">
          <LightRays
            raysOrigin="top-center"
            raysColor="#ffffff15"
            raysSpeed={1.8}
            lightSpread={1.5}
            rayLength={3.0}
            pulsating={true}
            followMouse={true}
            mouseInfluence={0.25}
            noiseAmount={0.08}
            distortion={0.1}
            fadeDistance={1.5}
            saturation={1.2}
          />
        </div>

        {/* Abstract Background Elements */}
        <div className="absolute top-0 right-0 w-[300px] sm:w-[600px] h-[300px] sm:h-[600px] bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 animate-pulse duration-[10000ms]" />
        <div className="absolute bottom-0 left-0 w-[250px] sm:w-[500px] h-[250px] sm:h-[500px] bg-gray-400/10 rounded-full blur-3xl translate-y-1/3 -translate-x-1/4" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 sm:px-4 sm:py-2 rounded-full bg-white/10 border border-gray-400/30 text-gray-200 text-xs sm:text-sm font-medium mb-6 sm:mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700 backdrop-blur-sm">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
              </span>
              <span className="hidden sm:inline">Now with AI-Powered Smart Matching</span>
              <span className="sm:hidden">AI Smart Matching</span>
            </div>

            <div className="mb-6 sm:mb-8">
              <Shuffle
                text="Find What You Lost."
                tag="h1"
                className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight"
                style={{
                  textAlign: 'center',
                  color: '#ffffff',
                  textShadow: '0 0 30px rgba(255, 255, 255, 0.3)',
                }}
                shuffleDirection="right"
                duration={0.5}
                animationMode="evenodd"
                shuffleTimes={2}
                ease="power3.out"
                stagger={0.04}
                threshold={0.2}
                triggerOnce={false}
                triggerOnHover={true}
                respectReducedMotion={true}
                scrambleCharset="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
                colorFrom="#ffffff"
                colorTo="#d1d5db"
              />
            </div>
            <style>
              {`
                @keyframes gradientShift {
                  0%, 100% { background-position: 0% 50%; }
                  50% { background-position: 100% 50%; }
                }
                .gradient-text {
                  background: linear-gradient(90deg, #ffffff, #d1d5db, #9ca3af, #d1d5db, #ffffff);
                  background-size: 200% auto;
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  background-clip: text;
                  animation: gradientShift 4s ease-in-out infinite;
                }
              `}
            </style>

            <h2 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 sm:mb-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200 gradient-text">
              Return What You Found.
            </h2>

            <p className="text-sm sm:text-base md:text-lg lg:text-xl text-gray-200 mb-6 sm:mb-8 md:mb-10 max-w-2xl mx-auto leading-relaxed px-2 sm:px-0 animate-in fade-in slide-in-from-bottom-10 duration-700 delay-300 drop-shadow-lg">
              A smart and secure platform designed to connect people, verify items, and reunite belongings with their rightful owners.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 px-4 sm:px-0 animate-in fade-in slide-in-from-bottom-10 duration-700 delay-300">
              <Button
                onClick={() => navigate('/report-lost')}
                className="w-full sm:w-auto h-12 sm:h-14 px-6 sm:px-8 rounded-full text-base sm:text-lg bg-black text-white hover:bg-gray-900 shadow-lg shadow-black/50 hover:shadow-black/70 transition-all hover:-translate-y-1 hover:scale-105 border border-gray-700"
              >
                Report Lost Item
              </Button>
              <Button
                onClick={() => navigate('/report-found')}
                variant="outline"
                className="w-full sm:w-auto h-12 sm:h-14 px-6 sm:px-8 rounded-full text-base sm:text-lg border-2 border-white/50 text-white hover:bg-white/10 hover:border-white transition-all hover:-translate-y-1 hover:scale-105 backdrop-blur-sm"
              >
                Report Found Item
              </Button>
            </div>
          </div>
        </div>

        {/* Subtle shadow for depth */}
        <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-b from-transparent to-black/5 z-20"></div>
      </section >

      {/* SECTION 2: Recently Found Items (Moved Up) */}
      < section className="min-h-screen w-full flex flex-col justify-center py-12 sm:py-16 md:py-20 bg-white" >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 sm:mb-10 md:mb-12 gap-3 sm:gap-4">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2 sm:mb-3 md:mb-4">Recently Found Items</h2>
              <p className="text-sm sm:text-base text-gray-600">Browse the latest items reported by our community.</p>
            </div>
            <Button variant="ghost" className="text-black hover:text-gray-800 text-sm sm:text-base" onClick={() => navigate('/items')}>
              View All <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 md:gap-6">
              {[1, 2, 3, 4].map((n) => <ItemCardSkeleton key={n} />)}
            </div>
          ) : error ? (
            <ErrorState message={error} onRetry={fetchItems} />
          ) : latestItems.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 md:gap-6">
              {latestItems.map((item) => (
                <ItemCard key={item.id} item={item} />
              ))}
            </div>
          ) : (
            <EmptyState
              title="No items found recently"
              description="Check back later or report an item yourself."
            />
          )}
        </div>
      </section >

      {/* SECTION 3: Features & How It Works (Moved Down) */}
      < section className="min-h-screen w-full flex flex-col justify-center py-12 sm:py-16 md:py-20 bg-gray-50" >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">

          {/* Feature Cards */}
          <div className="mb-12 sm:mb-16 md:mb-20">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 md:gap-6">
              <FeatureCard
                icon={Camera}
                title="Easy Reporting"
                description="Report instantly with photos."
              />
              <FeatureCard
                icon={BrainCircuit}
                title="Smart Matching"
                description="AI connects lost & found items."
              />
              <FeatureCard
                icon={ShieldCheck}
                title="Verified Claims"
                description="Secure community verification."
              />
              <FeatureCard
                icon={Bell}
                title="Real-Time Updates"
                description="Live alerts for matches."
              />
            </div>
          </div>

          {/* How It Works */}
          <div className="text-center mb-10 sm:mb-12 md:mb-16">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">How It Works</h2>
            <p className="text-sm sm:text-base text-gray-600 max-w-2xl mx-auto px-4 sm:px-0">
              Simple steps to get your items back. Fast, secure, and effective.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-8 left-[10%] right-[10%] h-0.5 bg-gradient-to-r from-gray-100 via-gray-300 to-gray-100" />

            <Step
              number="1"
              title="Post Item"
              description="Report details & photos."
            />
            <Step
              number="2"
              title="Smart Match"
              description="System finds matches."
            />
            <Step
              number="3"
              title="Connect"
              description="Verify ownership."
            />
            <Step
              number="4"
              title="Retrieve"
              description="Get your item back."
            />
          </div>
        </div>
      </section >

      {/* SECTION 4: CTA & Footer */}
      < section className="min-h-screen w-full flex items-center justify-center bg-white py-12 sm:py-16 md:py-20" >
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center w-full">
          <div className="bg-gradient-to-r from-black to-gray-900 rounded-2xl sm:rounded-3xl p-6 sm:p-8 md:p-12 shadow-2xl text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 sm:w-48 md:w-64 h-32 sm:h-48 md:h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/3 blur-3xl" />
            <div className="absolute bottom-0 left-0 w-32 sm:w-48 md:w-64 h-32 sm:h-48 md:h-64 bg-black/20 rounded-full translate-y-1/3 -translate-x-1/4 blur-3xl" />

            <div className="relative z-10">
              <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-4 sm:mb-6">Let's help lost things find their way home.</h2>
              <p className="text-gray-200 text-sm sm:text-base md:text-lg mb-8 sm:mb-10 max-w-2xl mx-auto px-2 sm:px-0">
                Join our growing community of helpers and finders. It only takes a minute to make a difference.
              </p>
              <Button
                onClick={() => navigate('/register')}
                className="w-full sm:w-auto h-12 sm:h-14 px-8 sm:px-10 rounded-full text-base sm:text-lg bg-white text-black hover:bg-gray-100 shadow-lg border-0 mb-8 sm:mb-10 md:mb-12"
              >
                Get Started Now
              </Button>

              {/* Trust Indicators */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6 md:gap-8">
                <SecurityFeature
                  icon={Users}
                  title="Verified Users"
                  description="Active moderation"
                />
                <SecurityFeature
                  icon={CheckCircle}
                  title="Community Driven"
                  description="Trusted finders"
                />
                <SecurityFeature
                  icon={Shield}
                  title="Secure Auth"
                  description="Enterprise security"
                />
                <div className="hidden sm:block">
                  <SecurityFeature
                    icon={Shield}
                    title="Safe Platform"
                    description="Privacy protected"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Simple Footer Links */}
          <div className="mt-8 sm:mt-12 flex flex-col md:flex-row justify-center gap-3 sm:gap-4 md:gap-8 text-gray-500 text-xs sm:text-sm">
            <a href="#" className="hover:text-blue-600 transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-blue-600 transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-blue-600 transition-colors">Contact Support</a>
            <span>© 2025 Lost & Found</span>
          </div>
        </div>
      </section >

    </div >
  );
};

// Sub-components
const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="bg-white p-4 sm:p-5 md:p-6 rounded-2xl border border-gray-100 shadow-lg hover:shadow-xl transition-all hover:-translate-y-1">
    <div className="w-10 h-10 sm:w-12 sm:h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-3 sm:mb-4 text-blue-600">
      <Icon className="w-5 h-5 sm:w-6 sm:h-6" />
    </div>
    <h3 className="text-base sm:text-lg font-bold text-gray-900 mb-1.5 sm:mb-2">{title}</h3>
    <p className="text-sm text-gray-600 leading-relaxed">{description}</p>
  </div>
);

const Step = ({ number, title, description }) => (
  <div className="relative flex flex-col items-center text-center z-10">
    <div className="w-12 h-12 sm:w-14 sm:h-14 bg-white border-4 border-blue-50 rounded-full flex items-center justify-center text-lg sm:text-xl font-bold text-blue-600 shadow-sm mb-3 sm:mb-4">
      {number}
    </div>
    <h3 className="text-base sm:text-lg font-bold text-gray-900 mb-1">{title}</h3>
    <p className="text-xs sm:text-sm text-gray-600">{description}</p>
  </div>
);

const SecurityFeature = ({ icon: Icon, title, description }) => (
  <div className="text-center">
    <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-3 text-white">
      <Icon className="w-6 h-6" />
    </div>
    <h3 className="font-bold text-white text-sm mb-1">{title}</h3>
    <p className="text-xs text-blue-100">{description}</p>
  </div>
);

export default Home;