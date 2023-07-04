import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { setTokenLocalStorage } from "../../utility/token";
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
