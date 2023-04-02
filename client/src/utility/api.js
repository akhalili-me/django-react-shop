import axios from "axios";
import { getToken } from "./token";
import { isAuthenticated, updateTokenIfExpired } from "./auth";

const API_BASE_URL = "http://127.0.0.1:8000/api/";

const authAxios = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    accept: "application/json",
  },
});

authAxios.interceptors.request.use(
  async (config) => {
    if (isAuthenticated()) {
      updateTokenIfExpired();
      const token = getToken();
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default authAxios;
