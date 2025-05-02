/*
axiosInstance.js

This file creates on Axios instance with interceptors to handle JWT tokens for authentication.
It checks if the token is expired before making a request and refreshes it if necessary.
It also handles 401 errors by attempting to refresh the token and retrying the request.
The code uses the jwt-decode library to decode the JWT token and check its expiration.
It is important to note that this code assumes the presence of a backend API that supports JWT authentication and provides endpoints for login, registration, and token refresh.
The code is structured to handle public endpoints separately, allowing unauthenticated access to certain routes like login and registration.
This code is a part of a larger application and should be used in conjunction with other components such as user authentication, registration, and token management.
*/

import axios from "axios";
import { jwtDecode } from "jwt-decode";

const isTokenExpired = (token) => {
  try {
    const decode = jwtDecode(token);
    const now = Date.now() / 1000;
    return decode.exp < now;
  } catch (err) {
    return true;
  }
};

const API = axios.create({
  baseURL: "http://localhost:8000/api/",
});

const publicEnpoints = ["users/login/", "users/register/"];

API.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("access");
    const refreshToken = localStorage.getItem("refresh");

    const fullUrl = new URL(config.url, API.defaults.baseURL).pathname;
    const isPublic = publicEnpoints.some((endpoint) =>
      fullUrl.endsWith(endpoint)
    );

    if (!isPublic && token) {
      if (isTokenExpired(token) && refreshToken) {
        try {
          const response = await axios.post("http://localhost:8000/api/users/token/refresh/", {
            refresh: refreshToken,
          });

          const { access, refresh } = response.data;
          localStorage.setItem("access", access);
          if (refresh) {
            localStorage.setItem("refresh", refresh);
          }

          config.headers.Authorization = `Bearer ${access}`;
          return config;
        } catch (err) {
          console.error("Falha ao renovar token antes da request:", err);
          localStorage.clear();
          window.location.href = "/login";
          return Promise.reject(err);
        }
      } else {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes("token/refresh/")
    ) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh");

        if (!refreshToken) {
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }

        const response = await axios.post("http://localhost:8000/api/users/token/refresh/", {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;
        localStorage.setItem("access", newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return API(originalRequest);
      } catch (refreshError) {
        console.error("Erro ao tentar renovar token:", refreshError);

        localStorage.clear();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default API;