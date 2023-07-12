import { createSlice } from "@reduxjs/toolkit";
import { getUserAddresses } from "./addressListReducers";

export const addressListSlice = createSlice({
	name: "addressList",
	initialState: { addresses: [], loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
		.addCase(getUserAddresses.pending, (state) => {
			state.loading = true;
		})
		.addCase(getUserAddresses.fulfilled, (state, action) => {
			state.loading = false;
			state.error = null;
			state.addresses = action.payload
		})
		.addCase(getUserAddresses.rejected, (state, action) => {
			state.loading = false;
			state.error = action.error.message;
		})
	},
});

export default addressListSlice.reducer;
