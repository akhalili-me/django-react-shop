import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";


export const register = createAsyncThunk(
	"auth/register",
	async ({ email, username, password }) => {
		try {
			const { data } = await authAxios.post("/accounts/users/", {
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

export const clearRegisterErrorsReducers = (state, action) => {
    state.error = null;
};