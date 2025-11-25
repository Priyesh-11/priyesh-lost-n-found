// Mock data for Lost & Found application

export const mockUsers = [
  {
    id: '1',
    email: 'john.doe@example.com',
    username: 'johndoe',
    fullName: 'John Doe',
    phone: '+1234567890',
    role: 'user',
    reputation: 85,
    isVerified: true,
    createdAt: '2024-01-15T10:30:00Z'
  },
  {
    id: '2',
    email: 'admin@lostandfound.com',
    username: 'admin',
    fullName: 'Admin User',
    phone: '+1234567891',
    role: 'admin',
    reputation: 100,
    isVerified: true,
    createdAt: '2024-01-01T08:00:00Z'
  }
];

export const mockItems = [
  {
    id: '1',
    title: 'Black Leather Wallet',
    description: 'Lost black leather wallet near Central Park. Contains ID cards and credit cards. Very important to me. Reward offered for return.',
    category: 'wallet',
    type: 'lost',
    status: 'active',
    location: 'Central Park, New York',
    date: '2024-03-15T14:30:00Z',
    images: ['https://images.unsplash.com/photo-1579014134953-1580d7f123f3'],
    contactInfo: {
      name: 'John Doe',
      email: 'john.doe@example.com',
      phone: '+1234567890'
    },
    userId: '1',
    createdAt: '2024-03-15T15:00:00Z',
    updatedAt: '2024-03-15T15:00:00Z'
  },
  {
    id: '2',
    title: 'Found Set of House Keys',
    description: 'Found a set of house keys with a blue keychain near the subway station on Main Street. Keys appear to be for a house or apartment.',
    category: 'keys',
    type: 'found',
    status: 'active',
    location: 'Main Street Subway Station',
    date: '2024-03-18T09:15:00Z',
    images: ['https://images.unsplash.com/flagged/photo-1564767609342-620cb19b2357'],
    contactInfo: {
      name: 'Sarah Smith',
      email: 'sarah.smith@example.com',
      phone: '+1234567892'
    },
    userId: '1',
    createdAt: '2024-03-18T10:00:00Z',
    updatedAt: '2024-03-18T10:00:00Z'
  },
  {
    id: '3',
    title: 'iPhone 14 Pro',
    description: 'Lost my iPhone 14 Pro with a black case at the coffee shop on 5th Avenue. Has a small crack on the screen. Please contact if found.',
    category: 'electronics',
    type: 'lost',
    status: 'active',
    location: '5th Avenue Coffee Shop',
    date: '2024-03-20T16:45:00Z',
    images: ['https://images.unsplash.com/photo-1511707171634-5f897ff02aa9'],
    contactInfo: {
      name: 'Michael Johnson',
      email: 'michael.j@example.com',
      phone: '+1234567893'
    },
    userId: '1',
    createdAt: '2024-03-20T17:00:00Z',
    updatedAt: '2024-03-20T17:00:00Z'
  },
  {
    id: '4',
    title: 'Red Leather Handbag',
    description: 'Found a beautiful red leather handbag at the bus stop near the library. Contains some personal items. Looking for the owner.',
    category: 'bag',
    type: 'found',
    status: 'active',
    location: 'Library Bus Stop',
    date: '2024-03-19T11:20:00Z',
    images: ['https://images.unsplash.com/photo-1584917865442-de89df76afd3'],
    contactInfo: {
      name: 'Emily Davis',
      email: 'emily.d@example.com',
      phone: '+1234567894'
    },
    userId: '1',
    createdAt: '2024-03-19T12:00:00Z',
    updatedAt: '2024-03-19T12:00:00Z'
  },
  {
    id: '5',
    title: 'Brown Wallet with Cash',
    description: 'Found a brown wallet containing some cash and cards near the park entrance. Trying to find the rightful owner.',
    category: 'wallet',
    type: 'found',
    status: 'active',
    location: 'City Park Entrance',
    date: '2024-03-21T08:30:00Z',
    images: ['https://images.unsplash.com/photo-1512358958014-b651a7ee1773'],
    contactInfo: {
      name: 'David Wilson',
      email: 'david.w@example.com',
      phone: '+1234567895'
    },
    userId: '1',
    createdAt: '2024-03-21T09:00:00Z',
    updatedAt: '2024-03-21T09:00:00Z'
  },
  {
    id: '6',
    title: 'Vintage Keys Collection',
    description: 'Lost a collection of vintage skeleton keys that have sentimental value. Last seen near the antique shop.',
    category: 'keys',
    type: 'lost',
    status: 'active',
    location: 'Antique Shop, Downtown',
    date: '2024-03-17T13:00:00Z',
    images: ['https://images.unsplash.com/photo-1609587415882-97552f39c6c2'],
    contactInfo: {
      name: 'Linda Martinez',
      email: 'linda.m@example.com',
      phone: '+1234567896'
    },
    userId: '1',
    createdAt: '2024-03-17T14:00:00Z',
    updatedAt: '2024-03-17T14:00:00Z'
  },
  {
    id: '7',
    title: 'iPhone on Table',
    description: 'Found an iPhone left on a table at the restaurant. Screen is unlocked. Please claim if this is yours.',
    category: 'electronics',
    type: 'found',
    status: 'active',
    location: 'Downtown Restaurant',
    date: '2024-03-22T19:30:00Z',
    images: ['https://images.unsplash.com/photo-1580910051074-3eb694886505'],
    contactInfo: {
      name: 'Robert Brown',
      email: 'robert.b@example.com',
      phone: '+1234567897'
    },
    userId: '1',
    createdAt: '2024-03-22T20:00:00Z',
    updatedAt: '2024-03-22T20:00:00Z'
  },
  {
    id: '8',
    title: 'Black Tote Bag',
    description: 'Lost my black tote bag with laptop inside at the train station. Very important work documents. Urgent!',
    category: 'bag',
    type: 'lost',
    status: 'active',
    location: 'Central Train Station',
    date: '2024-03-23T07:45:00Z',
    images: ['https://images.unsplash.com/photo-1614179689702-355944cd0918'],
    contactInfo: {
      name: 'Jennifer Taylor',
      email: 'jennifer.t@example.com',
      phone: '+1234567898'
    },
    userId: '1',
    createdAt: '2024-03-23T08:00:00Z',
    updatedAt: '2024-03-23T08:00:00Z'
  }
];

export const categories = [
  { value: 'all', label: 'All Categories' },
  { value: 'electronics', label: 'Electronics' },
  { value: 'wallet', label: 'Wallets' },
  { value: 'keys', label: 'Keys' },
  { value: 'bag', label: 'Bags' },
  { value: 'jewelry', label: 'Jewelry' },
  { value: 'documents', label: 'Documents' },
  { value: 'pets', label: 'Pets' },
  { value: 'other', label: 'Other' }
];

export const itemTypes = [
  { value: 'all', label: 'All' },
  { value: 'lost', label: 'Lost Items' },
  { value: 'found', label: 'Found Items' }
];

export const locations = [
  { value: 'library_main', label: 'Library' },
  { value: 'cafeteria_main', label: 'Cafeteria' },
  { value: 'gym_main', label: 'Near CDIPS' },
  { value: 'admin_block', label: 'Admin Block' },
  { value: 'lecture_hall_a', label: 'class room' },
  { value: 'lab_computer', label: 'Computer Labs' },
  { value: 'parking_main', label: 'Main Parking' },
  { value: 'other', label: 'Other Location' }
];

export const itemStatuses = [
  { value: 'active', label: 'Active' },
  { value: 'resolved', label: 'Resolved' },
  { value: 'expired', label: 'Expired' }
];

// Mock authentication state
export let mockAuthState = {
  isAuthenticated: false,
  user: null,
  token: null
};

// Mock authentication functions
export const mockLogin = (email, password) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const user = mockUsers.find(u => u.email === email);
      if (user && password === 'password123') {
        const token = 'mock-jwt-token-' + Date.now();
        mockAuthState = {
          isAuthenticated: true,
          user,
          token
        };
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(user));
        resolve({ success: true, user, token });
      } else {
        reject({ success: false, message: 'Invalid credentials' });
      }
    }, 500);
  });
};

export const mockRegister = (userData) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const newUser = {
        id: String(mockUsers.length + 1),
        ...userData,
        role: 'user',
        reputation: 0,
        isVerified: false,
        createdAt: new Date().toISOString()
      };
      mockUsers.push(newUser);
      const token = 'mock-jwt-token-' + Date.now();
      mockAuthState = {
        isAuthenticated: true,
        user: newUser,
        token
      };
      localStorage.setItem('authToken', token);
      localStorage.setItem('user', JSON.stringify(newUser));
      resolve({ success: true, user: newUser, token });
    }, 500);
  });
};

export const mockLogout = () => {
  mockAuthState = {
    isAuthenticated: false,
    user: null,
    token: null
  };
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
};

export const mockCheckAuth = () => {
  const token = localStorage.getItem('authToken');
  const userStr = localStorage.getItem('user');
  if (token && userStr) {
    const user = JSON.parse(userStr);
    mockAuthState = {
      isAuthenticated: true,
      user,
      token
    };
    return true;
  }
  return false;
};

// Initialize auth state from localStorage
mockCheckAuth();