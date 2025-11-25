import axios from 'axios';

// Hardcoded for production deployment - change for local development
const API_URL = 'https://priyesh-lost-n-found-backend.onrender.com/api/v1';

const api = axios.create({
    baseURL: API_URL,
    withCredentials: true,  // IMPORTANT: Required for CORS with credentials
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const authService = {
    login: async (email, password) => {
        const formData = new FormData();
        formData.append('username', email); // OAuth2 expects 'username'
        formData.append('password', password);
        const response = await api.post('/auth/login', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },
    register: async (userData) => {
        const response = await api.post('/auth/register', userData);
        return response.data;
    },
    getCurrentUser: async () => {
        const response = await api.get('/users/me');
        return response.data;
    },
    updateUser: async (userData) => {
        const response = await api.put('/users/me', userData);
        return response.data;
    },
    verifyEmail: async (token) => {
        const response = await api.post(`/auth/verify-email/${token}`);
        return response.data;
    },
    resendVerification: async (email) => {
        const response = await api.post('/auth/resend-verification', { email });
        return response.data;
    },
    forgotPassword: async (email) => {
        const response = await api.post('/auth/forgot-password', { email });
        return response.data;
    },
    resetPassword: async (token, new_password) => {
        const response = await api.post('/auth/reset-password', { token, new_password });
        return response.data;
    }
};

export const itemsService = {
    getAll: async (params) => {
        const response = await api.get('/items', { params });
        return response.data;
    },
    getById: async (id) => {
        const response = await api.get(`/items/${id}`);
        return response.data;
    },
    create: async (itemData) => {
        const response = await api.post('/items', itemData);
        return response.data;
    },
    update: async (id, itemData) => {
        const response = await api.put(`/items/${id}`, itemData);
        return response.data;
    },
    delete: async (id) => {
        const response = await api.delete(`/items/${id}`);
        return response.data;
    },
    uploadImages: async (id, formData) => {
        const response = await api.post(`/items/${id}/images`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },
    uploadClaimProof: async (id, formData) => {
        const response = await api.post(`/items/${id}/claim-proof-upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    },
    resolve: async (id) => {
        const response = await api.put(`/admin/items/${id}/resolve`);
        return response.data;
    },
    getMatches: async (id) => {
        const response = await api.get(`/items/${id}/matches`);
        return response.data;
    }
};

export const categoriesService = {
    getAll: async () => {
        try {
            const response = await api.get('/items/categories');
            return response.data;
        } catch (error) {
            console.warn("Failed to fetch categories", error);
            return [];
        }
    }
};

export const claimsService = {
    create: async (itemId, claimData) => {
        const response = await api.post(`/items/${itemId}/claim`, claimData);
        return response.data;
    },
    getMyClaims: async () => {
        const response = await api.get('/claims/my-claims');
        return response.data;
    },
    getAll: async (params) => { // Admin only
        const response = await api.get('/admin/claims', { params });
        return response.data;
    },
    verify: async (id, data) => { // Admin only
        const response = await api.put(`/admin/claims/${id}/verify`, data);
        return response.data;
    }
};

export default api;
