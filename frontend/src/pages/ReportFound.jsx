import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Card } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { locations, categories } from '../utils/mock';
import { itemsService, categoriesService } from '../services/api';
import { Upload, X, Loader2 } from 'lucide-react';
import { ShineBorder } from '../components/ui/shine-border';
import { useToast } from '../hooks/use-toast';

const ReportFound = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    location: '',
    customLocation: '',
    date: '',
    contactName: '',
    contactEmail: '',
    contactPhone: ''
  });
  const [images, setImages] = useState([]);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [categoryList, setCategoryList] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const cats = await categoriesService.getAll();
        if (cats && cats.length > 0) {
          const formattedCats = cats.map(c => ({ value: c.name.toLowerCase(), label: c.name, id: c.id }));
          setCategoryList(formattedCats);
        } else {
          setCategoryList(categories.filter(c => c.value !== 'all'));
        }
      } catch (error) {
        console.error("Failed to fetch categories", error);
        setCategoryList(categories.filter(c => c.value !== 'all'));
      }
    };
    fetchCategories();
  }, []);

  // Helper to map category value to ID
  const getCategoryId = (value) => {
    const category = categoryList.find(c => c.value === value);
    return category ? category.id : 9; // Default to 'other'
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title || formData.title.length < 5) {
      newErrors.title = 'Title must be at least 5 characters';
    }

    if (!formData.description || formData.description.length < 20) {
      newErrors.description = 'Description must be at least 20 characters';
    }

    if (!formData.category) {
      newErrors.category = 'Please select a category';
    }

    if (!formData.location) {
      newErrors.location = 'Please select a location';
    } else if (formData.location === 'other' && (!formData.customLocation || formData.customLocation.length < 3)) {
      newErrors.customLocation = 'Please specify the location (at least 3 characters)';
    }

    if (!formData.date) {
      newErrors.date = 'Date is required';
    }

    if (!formData.contactName) {
      newErrors.contactName = 'Contact name is required';
    }

    if (!formData.contactEmail || !/\S+@\S+\.\S+/.test(formData.contactEmail)) {
      newErrors.contactEmail = 'Valid email is required';
    }

    if (!formData.contactPhone) {
      newErrors.contactPhone = 'Contact phone is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    if (images.length + files.length > 5) {
      toast({
        title: 'Too many images',
        description: 'You can upload maximum 5 images',
        variant: 'destructive'
      });
      return;
    }

    const newImages = files.map((file) => ({
      file,
      preview: URL.createObjectURL(file)
    }));
    setImages(prev => [...prev, ...newImages]);
  };

  const removeImage = (index) => {
    setImages(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      // 1. Create Item
      const itemData = {
        title: formData.title,
        description: formData.description,
        category_id: getCategoryId(formData.category),
        type: 'found',
        status: 'active',
        location: formData.location === 'other' ? formData.customLocation : locations.find(l => l.value === formData.location)?.label || formData.location,
        date_lost: new Date(formData.date).toISOString(), // Backend expects ISO string and uses date_lost for both
        contact_method: `Name: ${formData.contactName}, Email: ${formData.contactEmail}, Phone: ${formData.contactPhone}`
      };

      const newItem = await itemsService.create(itemData);

      // 2. Upload Images
      if (images.length > 0) {
        const imageFormData = new FormData();
        images.forEach((img) => {
          imageFormData.append('files', img.file);
        });
        await itemsService.uploadImages(newItem.id, imageFormData);
      }

      toast({
        title: 'Item reported successfully!',
        description: 'Your found item has been posted. The owner can now contact you.'
      });
      navigate('/dashboard');
    } catch (error) {
      console.error("Failed to report item:", error);
      toast({
        title: "Error",
        description: "Failed to report item. Please try again.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Report Found Item</h1>
          <p className="text-gray-600">Help reunite someone with their belongings</p>
        </div>

        <Card className="relative overflow-hidden p-6">
          <ShineBorder shineColor={["#2563eb", "#60a5fa", "#93c5fd"]} borderWidth={2} />
          <form onSubmit={handleSubmit} className="space-y-6 relative z-10">
            {/* Title */}
            <div className="space-y-2">
              <Label htmlFor="title">Item Title *</Label>
              <Input
                id="title"
                name="title"
                placeholder="e.g., Found Set of Keys"
                value={formData.title}
                onChange={handleChange}
                className={errors.title ? 'border-red-500' : ''}
              />
              {errors.title && (
                <p className="text-sm text-red-600">{errors.title}</p>
              )}
            </div>

            {/* Category */}
            <div className="space-y-2">
              <Label htmlFor="category">Category *</Label>
              <Select value={formData.category} onValueChange={(value) => setFormData(prev => ({ ...prev, category: value }))}>
                <SelectTrigger className={errors.category ? 'border-red-500' : ''}>
                  <SelectValue placeholder="Select a category" />
                </SelectTrigger>
                <SelectContent>
                  {categoryList.map((cat) => (
                    <SelectItem key={cat.value} value={cat.value}>
                      {cat.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.category && (
                <p className="text-sm text-red-600">{errors.category}</p>
              )}
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description">Description *</Label>
              <Textarea
                id="description"
                name="description"
                placeholder="Provide detailed description of the found item..."
                value={formData.description}
                onChange={handleChange}
                rows={5}
                className={errors.description ? 'border-red-500' : ''}
              />
              {errors.description && (
                <p className="text-sm text-red-600">{errors.description}</p>
              )}
            </div>

            {/* Location */}
            {/* Location Selection */}
            <div className="space-y-2">
              <Label htmlFor="location">Location Found</Label>
              <Select
                value={formData.location}
                onValueChange={(value) => setFormData({ ...formData, location: value })}
              >
                <SelectTrigger className={errors.location ? 'border-red-500' : ''}>
                  <SelectValue placeholder="Select location" />
                </SelectTrigger>
                <SelectContent>
                  {locations.map((loc) => (
                    <SelectItem key={loc.value} value={loc.value}>
                      {loc.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.location && (
                <p className="text-sm text-red-500">{errors.location}</p>
              )}
            </div>

            {/* Custom Location Input (shown if 'other' is selected) */}
            {formData.location === 'other' && (
              <div className="space-y-2 animate-in fade-in slide-in-from-top-2 duration-200">
                <Label htmlFor="customLocation">Specific Location Details</Label>
                <Input
                  id="customLocation"
                  placeholder="E.g., Near the vending machine on 2nd floor"
                  value={formData.customLocation}
                  onChange={(e) => setFormData({ ...formData, customLocation: e.target.value })}
                  className={errors.customLocation ? 'border-red-500' : ''}
                />
                {errors.customLocation && (
                  <p className="text-sm text-red-500">{errors.customLocation}</p>
                )}
              </div>
            )}

            {/* Date */}
            <div className="space-y-2">
              <Label htmlFor="date">Date Found *</Label>
              <Input
                id="date"
                name="date"
                type="datetime-local"
                value={formData.date}
                onChange={handleChange}
                className={errors.date ? 'border-red-500' : ''}
              />
              {errors.date && (
                <p className="text-sm text-red-600">{errors.date}</p>
              )}
            </div>

            {/* Image Upload */}
            <div className="space-y-2">
              <Label>Upload Images (Max 5)</Label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  onChange={handleImageUpload}
                  className="hidden"
                  id="image-upload"
                  disabled={images.length >= 5}
                />
                <label htmlFor="image-upload" className="cursor-pointer">
                  <Upload className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    PNG, JPG up to 5MB ({images.length}/5)
                  </p>
                </label>
              </div>
              {images.length > 0 && (
                <div className="grid grid-cols-3 gap-3 mt-3">
                  {images.map((img, index) => (
                    <div key={index} className="relative group">
                      <img
                        src={img.preview}
                        alt={`Upload ${index + 1}`}
                        className="w-full h-24 object-cover rounded-lg"
                      />
                      <button
                        type="button"
                        onClick={() => removeImage(index)}
                        className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Contact Information */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="contactName">Name *</Label>
                  <Input
                    id="contactName"
                    name="contactName"
                    placeholder="Your name"
                    value={formData.contactName}
                    onChange={handleChange}
                    className={errors.contactName ? 'border-red-500' : ''}
                  />
                  {errors.contactName && (
                    <p className="text-sm text-red-600">{errors.contactName}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="contactEmail">Email *</Label>
                  <Input
                    id="contactEmail"
                    name="contactEmail"
                    type="email"
                    placeholder="your.email@example.com"
                    value={formData.contactEmail}
                    onChange={handleChange}
                    className={errors.contactEmail ? 'border-red-500' : ''}
                  />
                  {errors.contactEmail && (
                    <p className="text-sm text-red-600">{errors.contactEmail}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="contactPhone">Phone *</Label>
                  <Input
                    id="contactPhone"
                    name="contactPhone"
                    type="tel"
                    placeholder="+1234567890"
                    value={formData.contactPhone}
                    onChange={handleChange}
                    className={errors.contactPhone ? 'border-red-500' : ''}
                  />
                  {errors.contactPhone && (
                    <p className="text-sm text-red-600">{errors.contactPhone}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex gap-3 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate(-1)}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button type="submit" disabled={loading} className="flex-1">
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Submitting...
                  </>
                ) : (
                  'Report Found Item'
                )}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default ReportFound;