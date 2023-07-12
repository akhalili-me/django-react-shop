import { createSlice } from "@reduxjs/toolkit";
import { refreshAndSetAccessToken } from "./tokenReducers";

export const tokenSlice = createSlice({
	name: "token",
	initialState: {
		loading: null,
		error: null,
		success: null,
	},
	reducers: { 
	},
	extraReducers: (builder) => {
		builder

			// refresh access token
			.addCase(refreshAndSetAccessToken.pending, (state) => {
				state.loading = true;
			})
			.addCase(refreshAndSetAccessToken.fulfilled, (state, action) => {
				state.loading = false;
				state.success = true;
				state.error = null;
			})
			.addCase(refreshAndSetAccessToken.rejected, (state, action) => {
				state.loading = false;
                state.success = false;
				state.error = action.error.message;
			})
	},
});

export default tokenSlice.reducer;
