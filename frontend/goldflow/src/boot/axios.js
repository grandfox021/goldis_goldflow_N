// src/boot/axios.js
import axios from 'axios';
import { boot } from 'quasar/wrappers';
import { useAuthStore } from 'src/stores/auth'; // Import auth store

// Create axios instance
const api = axios.create({
  baseURL:'http://localhost:8080',
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;

  },
  (error) => {
    return Promise.reject(error);
  }
);


api.interceptors.response.use(
  (response) => response,
  async (error) => {


    if (error.response?.status === 401 ) {

      const authStore = useAuthStore();
      if(!authStore.isAuthenticated){
        authStore.logout()
      }



      return Promise.reject(error);
    }

    if (error.response?.status === 403) {
      console.error('Forbidden request:', error);
    } else if (error.response?.status === 422) {
      console.error('Validation error:', error.response.data);
    } else if (error.response?.status === 500) {
      console.error('Server error:', error);
    }

    return Promise.reject(error);
  }
);

export default boot(({ app }) => {
  app.config.globalProperties.$api = api;
});

export { api };
