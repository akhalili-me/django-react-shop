import { createSlice } from "@reduxjs/toolkit";
import { login, register, logoutReducer, clearLoginErrorsReducer } from "./loginReducers";

export const loginSlice = createSlice({
	name: "login",
	initialState: {
		authenticated: false,
		loading: null,
		error: null,
		username: null,
		email: null,
	},
	reducers: {
		logout: logoutReducer,
		clearLoginErrors: clearLoginErrorsReducer
	},
	extraReducers: (builder) => {
		builder
			// Login
			.addCase(login.pending, (state) => {
				state.loading = true;
			})
			.addCase(login.fulfilled, (state, action) => {
				state.loading = false;
				state.username = action.payload.username;
				state.email = action.payload.email;
				state.authenticated = true
			})
			.addCase(login.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			});
	},
});

export const { logout,clearLoginErrors } = loginSlice.actions;
export default loginSlice.reducer;
