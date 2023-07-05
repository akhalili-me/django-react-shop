import { createSlice } from "@reduxjs/toolkit";
import { login, register, logoutReducer } from "./authReducers";

export const authSlice = createSlice({
	name: "auth",
	initialState: {
		authenticated: false,
		loading: null,
		error: null,
		username: null,
		email: null,
		registered: false,
	},
	reducers: {
		logout: logoutReducer,
	},
	extraReducers: (builder) => {
		builder

			// Register
			.addCase(register.pending, (state) => {
				state.loading = true;
			})
			.addCase(register.fulfilled, (state, action) => {
				state.loading = false;
				state.registered = true;
			})
			.addCase(register.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})

			// Login
			.addCase(login.pending, (state) => {
				state.loading = true;
				state.registered = false;
			})
			.addCase(login.fulfilled, (state, action) => {
				state.loading = false;
				state.authenticated = true;
				state.username = action.payload.username;
				state.email = action.payload.email;
			})
			.addCase(login.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			});
	},
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;
