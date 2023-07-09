import { createSlice } from "@reduxjs/toolkit";
import { addAddress,udpateAddress,deleteAddress } from "./addressOperationsReducers";

export const addressOperationsSlice = createSlice({
	name: "AddressOperations",
	initialState: { loading: null, error: null, success: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addMatcher(
				(action) =>
					[
						addAddress.pending,
						udpateAddress.pending,
						deleteAddress.pending,
					].includes(action.type),
				(state) => {
					state.loading = true;
					state.success = null;
				}
			)
			.addMatcher(
				(action) =>
					[
						addAddress.fulfilled,
						udpateAddress.fulfilled,
						deleteAddress.fulfilled,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.success = true;
				}
			)
			.addMatcher(
				(action) =>
					[
						addAddress.rejected,
						udpateAddress.rejected,
						deleteAddress.rejected,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.success = false;
					state.error = action.error.message;
				}
			);
	},
});

export default addressOperationsSlice.reducer;
