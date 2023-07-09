import { createSlice } from "@reduxjs/toolkit";
import { getUserAddresses } from "./addressListReducers";

export const addressListSlice = createSlice({
	name: "addressList",
	initialState: { addresses: [], loading: null, error: null, count: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addMatcher(
				(action) =>
					[
						getUserAddresses.pending,
					].includes(action.type),
				(state) => {
					state.loading = true;
				}
			)
			.addMatcher(
				(action) =>
					[
						getUserAddresses.fulfilled,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.addresses = action.payload.results;
					state.count = action.payload.count;
				}
			)
			.addMatcher(
				(action) =>
					[
						getUserAddresses.rejected,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.error = action.error.message;
				}
			);
	},
});

export default addressListSlice.reducer;
