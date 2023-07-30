import { createSlice } from "@reduxjs/toolkit";
import {getProductsByFilter } from "./productListReducers";

export const productListSlice = createSlice({
	name: "productList",
	initialState: { products: [], loading: null, error: null, count: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch products by filter
			.addCase(getProductsByFilter.pending, (state) => {
				state.loading = true;
			})
			.addCase(getProductsByFilter.fulfilled, (state, action) => {
				state.loading = false;
				state.error = null;
                state.products = action.payload.results;
                state.count = action.payload.count;
			})
			.addCase(getProductsByFilter.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			});
	},
});

export default productListSlice.reducer;
