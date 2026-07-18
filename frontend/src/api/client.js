import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30s
});

// Request Interceptor: Attach JWT Token
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('hydrogrow_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Handle JWT Expiration & Error Retry Logic
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized (Expired or Invalid JWT Token)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('hydrogrow_token');
    }

    // Network Retry Support for Transient Failures (1 retry)
    if (!error.response && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        return await client(originalRequest);
      } catch (retryErr) {
        return Promise.reject(retryErr);
      }
    }

    return Promise.reject(error);
  }
);

export default client;
