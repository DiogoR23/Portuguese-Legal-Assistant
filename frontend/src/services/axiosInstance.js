import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api/",
});

const publicEndpoints = ['users/register/', 'users/login/'];

API.interceptors.request.use(
  (config) => {
    const isPublic = publicEndpoints.some((endpoint) =>
      config.url.includes(endpoint)
    );

    if (!isPublic) {
      const token = localStorage.getItem("access");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    console.log('[AXIOS]', config);

    return config;
  },
  (error) => Promise.reject(error)
);

export default API;
