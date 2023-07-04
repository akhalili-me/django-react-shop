import { createSlice } from "@reduxjs/toolkit";
import { login } from "./authReducers";

export const authSlice = createSlice({
	name: "auth",
	initialState: {
		authenticated: false,
		loading: null,
		error: null,
		username: null,
		email: null,
	},
	reducers: {},
	extraReducers: (builder) => {
        // Login
		builder
			.addCase(login.pending, (state) => {
				state.loading = true;
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

export default authSlice.reducer;
