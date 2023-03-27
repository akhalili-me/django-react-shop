export const TOKEN_KEY = "access_token";
export const REFRESH_TOKEN_KEY = "refresh_token";

export const setToken = (tokenData) => {
  localStorage.setItem(TOKEN_KEY, tokenData.access);
  localStorage.setItem(REFRESH_TOKEN_KEY, tokenData.refresh);
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const getRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

export const getJwtTokens = () => {
  const token = getToken();
  const refreshToken = getRefreshToken();
  return { token, refreshToken };
};

export const removeTokens = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

export const isTokenExpired = (token) => {
  const decodedToken = JSON.parse(atob(token.split(".")[1]));
  return decodedToken.exp <= Date.now() / 1000;
};
