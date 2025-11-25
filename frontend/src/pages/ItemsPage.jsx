import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import ItemCard from '../components/items/ItemCard';
import ItemCardSkeleton from '../components/items/ItemCardSkeleton';
import EmptyState from '../components/common/EmptyState';
import ErrorState from '../components/common/ErrorState';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { itemsService, categoriesService } from '../services/api';
import { categories, itemTypes } from '../utils/mock';
import { Search, Filter, X, Package } from 'lucide-react';
import { useToast } from '../hooks/use-toast';

const ItemsPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [items, setItems] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [showFilters, setShowFilters] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchItems = async () => {
    setLoading(true);
    setError(null);
    try {
      // Build query parameters with defaults
      const params = {};

      // Status: default to 'active' unless explicitly specified
      const statusParam = searchParams.get('status');
      if (statusParam) {
        params.status = statusParam;
      } else {
        params.status = 'active';  // Default to active items only
      }

      // Type filter
      const typeParam = searchParams.get('type');
      if (typeParam && typeParam !== 'all') {
        params.type = typeParam;
      }
      // If no type param or 'all', we don't send type to API, assuming API returns all types by default

      // Search query
      const searchQuery = searchParams.get('search');
      if (searchQuery) {
        params.query = searchQuery;
      }

      const data = await itemsService.getAll(params);
      const fetchedItems = Array.isArray(data) ? data : data.items || [];
      // Transform to match existing structure if needed
      const mappedItems = fetchedItems.map(item => ({
        ...item,
        category: item.category ? item.category.name : 'other', // Map category object to name for filtering
        images: item.images && item.images.length > 0 ? item.images.map(img => img.image_url) : [],
        date: item.date_lost || item.date_found || item.created_at // Map date fields
      }));
      setItems(mappedItems);
      setFilteredItems(mappedItems);
    } catch (err) {
      console.error("Failed to fetch items:", err);
      setError(err.message || 'Failed to load items');
      toast({
        title: "Error",
        description: "Failed to load items. Please try again.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [searchParams]);

  useEffect(() => {
    filterItems();
  }, [searchQuery, selectedCategory, selectedType, items]);

  const filterItems = () => {
    let filtered = [...items];

    // Search filter
    if (searchQuery) {
      filtered = filtered.filter(
        (item) =>
          item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.location.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Category filter
    if (selectedCategory !== 'all') {
      filtered = filtered.filter((item) => item.category === selectedCategory);
    }

    // Type filter
    if (selectedType !== 'all') {
      filtered = filtered.filter((item) => item.type === selectedType);
    }

    // Sort by date (newest first)
    filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

    setFilteredItems(filtered);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery) {
      setSearchParams({ search: searchQuery });
    } else {
      setSearchParams({});
    }
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedType('all');
    setSearchParams({});
  };

  const hasActiveFilters = searchQuery || selectedCategory !== 'all' || selectedType !== 'all';

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Browse Items</h1>
          <p className="text-gray-600">Search through lost and found items</p>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="mb-4">
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <Input
                  type="text"
                  placeholder="Search items by title, description, or location..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Button type="submit">
                Search
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowFilters(!showFilters)}
                className="md:hidden"
              >
                <Filter className="w-4 h-4" />
              </Button>
            </div>
          </form>

          {/* Filters */}
          <div className={`grid grid-cols-1 md:grid-cols-3 gap-4 ${showFilters ? '' : 'hidden md:grid'}`}>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((cat) => (
                    <SelectItem key={cat.value} value={cat.value}>
                      {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Type</label>
              <Select value={selectedType} onValueChange={setSelectedType}>
                <SelectTrigger>
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  {itemTypes.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-end">
              {hasActiveFilters && (
                <Button
                  variant="outline"
                  onClick={clearFilters}
                  className="w-full"
                >
                  <X className="w-4 h-4 mr-2" />
                  Clear Filters
                </Button>
              )}
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="mb-4">
          <p className="text-gray-600">
            Showing <span className="font-semibold">{filteredItems.length}</span> items
          </p>
        </div>

        {/* Conditional Rendering: Loading / Error / Empty / Items */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(9)].map((_, index) => (
              <ItemCardSkeleton key={index} />
            ))}
          </div>
        ) : error ? (
          <ErrorState
            title="Failed to Load Items"
            message={error}
            onRetry={fetchItems}
          />
        ) : filteredItems.length === 0 ? (
          <EmptyState
            icon={Package}
            title="No Items Found"
            description={items.length === 0
              ? "There are no active items at the moment."
              : "No items match your current filters. Try adjusting your search criteria."
            }
            actionLabel="Clear Filters"
            onAction={() => {
              setSearchQuery('');
              setSelectedCategory('all');
              setSelectedType('all');
            }}
            secondaryActionLabel="Report New Item"
            onSecondaryAction={() => navigate('/report-lost')}
          />
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredItems.map((item) => (
                <ItemCard key={item.id} item={item} />
              ))}
            </div>
            {hasActiveFilters && (
              <Button onClick={clearFilters} variant="outline" className="mt-6">
                Clear All Filters
              </Button>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ItemsPage;