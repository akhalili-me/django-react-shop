import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { removeTokensLocalStorage, setTokenLocalStorage } from "../../utility/token";
import jwt_decode from "jwt-decode";

export const login = createAsyncThunk(
	"auth/login",
	async ({ email, password }) => {
		try {
			const { data } = await axios.post("/accounts/token", {
				email,
				password,
			});

			setTokenLocalStorage(data);
			const decodedToken = jwt_decode(data.access);
			return {
				username: decodedToken.username,
				email: decodedToken.email,
			};
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const register = createAsyncThunk(
	"auth/register",
	async ({ email, username, password }) => {
		try {
			const { data } = await axios.post("/accounts/users", {
				email,
				username,
				password,
			});
			return data;
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const logoutReducer = (state, action) => {
	removeTokensLocalStorage();
	state.authenticated = false;
	state.email = null;
	state.username = null;
	state.registered = null;
	window.location.replace("/");
};

export const clearAuthErrorsReducer = (state, action) => {
	state.error = null;
};