export const ACCESS_TOKEN_KEY = "access_token";
export const REFRESH_TOKEN_KEY = "refresh_token";

export const setAccessTokenLocalStorage = (accessToken) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
}

export const setBothJwtTokenLocalStorage = (tokenData) => {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokenData.access);
  localStorage.setItem(REFRESH_TOKEN_KEY, tokenData.refresh);
};

export const getAccessToken = () => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

export const getRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

export const getBothJwtTokenLocalStorage = () => {
  const accessToken = getAccessToken();
  const refreshToken = getRefreshToken();
  return { accessToken, refreshToken };
};

export const removeJWTTokensLocalStorage = () => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

export const isTokenExpired = (token) => {
  const decodedToken = JSON.parse(atob(token.split(".")[1]));
  return decodedToken.exp <= Date.now() / 1000;
};

export const isAuthenticated = () => {
  const { token, refreshToken } = getBothJwtTokenLocalStorage();

  if (!refreshToken || !token || isTokenExpired(refreshToken)) {
    return false;
  }

  return true;
};
