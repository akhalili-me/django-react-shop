import { createSlice } from "@reduxjs/toolkit";
import { addAddress,updateAddress,deleteAddress } from "./addressOperationsReducers";

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
						updateAddress.pending,
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
						updateAddress.fulfilled,
						deleteAddress.fulfilled,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.success = true;
					state.error = null;
				}
			)
			.addMatcher(
				(action) =>
					[
						addAddress.rejected,
						updateAddress.rejected,
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
