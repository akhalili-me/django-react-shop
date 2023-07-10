import { createAsyncThunk } from "@reduxjs/toolkit";
import { removeTokensLocalStorage, setTokenLocalStorage } from "../../../utility/token";
import jwt_decode from "jwt-decode";
import authAxios from "../../../utility/api";

export const login = createAsyncThunk(
	"auth/login",
	async ({ email, password }) => {
		try {
			const { data } = await authAxios.post("/accounts/token", {
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

export const logoutReducer = (state, action) => {
	removeTokensLocalStorage();
	state.authenticated = false;
	state.email = null;
	state.username = null;
	state.registered = null;
	window.location.replace("/");
};

export const clearLoginErrorsReducer = (state, action) => {
	state.error = null;
};