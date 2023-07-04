import axios from "axios";
import {
  getJwtTokens,
  removeTokens,
  isTokenExpired,
  TOKEN_KEY,
} from "./token";

export const register = async (email, username, password) => {
  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/api/accounts/users/",
      {
        email,
        username,
        password,
      }
    );

    return response;
  } catch (error) {
    return error.response;
  }
};

export const logout = () => {
  removeTokens();
  window.location.replace("/");
};

export const isAuthenticated = () => {
  const { token, refreshToken } = getJwtTokens();

  if (!refreshToken || !token || isTokenExpired(refreshToken)) {
    return false;
  }

  return true;
};

export const updateTokenIfExpired = () => {
  const { token, refreshToken } = getJwtTokens();

  if (isTokenExpired(token) && isTokenExpired(refreshToken) === false) {
    updateTokenKey(refreshToken);
  }
};

const updateTokenKey = async (refToken) => {
  try {
    const { data } = await axios.post("/accounts/token/refresh", {
      refresh: refToken,
    });
    localStorage.setItem(TOKEN_KEY, data.access);
  } catch (error) {
    return error.response;
  }
};
