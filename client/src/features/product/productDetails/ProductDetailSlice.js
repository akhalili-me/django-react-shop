import { createSlice } from "@reduxjs/toolkit";
import { getProductDetails } from "./productDetailsReducers";

export const productDetailsSlice = createSlice({
	name: "productDetails",
	initialState: { product: {}, loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch latest products
			.addCase(getProductDetails.pending, (state) => {
				state.loading = true;
			})
			.addCase(getProductDetails.fulfilled, (state, action) => {
				state.loading = false;
				state.error = null;
                state.product = action.payload
			})
			.addCase(getProductDetails.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export default productDetailsSlice.reducer;
