import { createSlice } from "@reduxjs/toolkit";
import { getAddressById } from "./addressDetailsReducers";

export const AddressDetailsSlice = createSlice({
	name: "addressDetails",
	initialState: { address: {}, loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch address by id
			.addCase(getAddressById.pending, (state) => {
				state.loading = true;
			})
			.addCase(getAddressById.fulfilled, (state, action) => {
				state.loading = false;
                state.address = action.payload
			})
			.addCase(getAddressById.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export default AddressDetailsSlice.reducer;