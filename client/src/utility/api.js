import axios from "axios";
import { getToken, isTokenExpired } from "./token";
import { getAccessToken } from "./token";

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
      const accessToken = getAccessToken();
      if (accessToken && isTokenExpired(accessToken) === false) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
    return config;
  },
  (error) => Promise.reject(error)
);

export default authAxios;
