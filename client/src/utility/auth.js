import axios from "axios"
import {setToken,getBothTokens,getToken,removeTokens,isTokenExpired,TOKEN_KEY,getRefreshToken} from './token'

export const logout = () => {
    removeTokens()
    window.location.replace('/');
}

export const login = async (email,password) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/accounts/token',{
            email,
            password,
        })

        setToken(response.data)

        return response;
    } catch (error) {
        return error.response
    }
}

export const register = async (email,username,password) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/accounts/',{
            email,
            username,
            password,
        })

        return response;
    } catch (error) {
        return error.response
    }
}

export const checkAndUpdateTokenKey = () => {
    const refToken = getRefreshToken()
    if (refToken && isTokenExpired(refToken) === false) {
        updateTokenKey(refToken)
    }
}

const updateTokenKey = async (refToken) => {
    try {
        const {data} = await axios.post('/accounts/token/refresh',{
            refresh: refToken
        })
        localStorage.setItem(TOKEN_KEY, data.access)
    } catch (error) {
        return error.response
    }
}

export const isAuthenticated = () => {
    const { token, refreshToken } = getBothTokens();

    if (!refreshToken) {
        return false
    }

    if (!isTokenExpired(token)) {
        return true;
    } else if (!isTokenExpired(refreshToken)) {
        updateTokenKey(refreshToken)
        return true
    } 

    return false
}

const axiosInstance = axios.create({
    timeout: 5000,
    headers:{
        'Content-Type': 'application/json',
        accept: 'application/json',
    }
})

axiosInstance.interceptors.request.use(
(config) => {
    if (isAuthenticated() === true) {
        const token = getToken()
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
},
(error) => Promise.reject(error),
);

export default axiosInstance;