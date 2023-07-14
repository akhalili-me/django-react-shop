import { createSlice } from "@reduxjs/toolkit";
import { getChildCategoriesWithTopSoldProducts } from "./childCategoryProductsReducers";

export const productDetailsSlice = createSlice({
	name: "productDetails",
	initialState: { childCategory: [], parentCategory: null, loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch top sold products of child category by parent category id
			.addCase(getChildCategoriesWithTopSoldProducts.pending, (state) => {
				state.loading = true;
			})
			.addCase(getChildCategoriesWithTopSoldProducts.fulfilled, (state, action) => {
				state.loading = false;
				state.error = null;
                state.parentCategory = action.payload[0].parent
                state.childCategory = action.payload
			})
			.addCase(getChildCategoriesWithTopSoldProducts.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export default productDetailsSlice.reducer;
