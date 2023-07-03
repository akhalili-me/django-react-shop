import { createSlice } from "@reduxjs/toolkit";
import { getLatestProducts,getProductsByFilter } from "./productReducers";

export const productSlice = createSlice({
	name: "product",
	initialState: { products: [], loading: null, error: "", count: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch latest products
			.addCase(getLatestProducts.pending, (state) => {
				state.loading = true;
			})
			.addCase(getLatestProducts.fulfilled, (state, action) => {
				state.loading = false;
                state.products = action.payload.results
                state.count = action.payload.count;
			})
			.addCase(getLatestProducts.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})

			// Fetch products by filter
			.addCase(getProductsByFilter.pending, (state) => {
				state.loading = true;
			})
			.addCase(getProductsByFilter.fulfilled, (state, action) => {
				state.loading = false;
                state.products = action.payload.results;
                state.count = action.payload.count;
			})
			.addCase(getProductsByFilter.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			});
	},
});

export default productSlice.reducer;
