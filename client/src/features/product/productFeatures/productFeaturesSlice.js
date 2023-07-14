import { createSlice } from "@reduxjs/toolkit";
import { getProductFeatures } from "./productFeaturesReducers";

export const productFeaturesSlice = createSlice({
	name: "productFeatures",
	initialState: { features: [], loading: null, error: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch product features
			.addCase(getProductFeatures.pending, (state) => {
				state.loading = true;
			})
			.addCase(getProductFeatures.fulfilled, (state, action) => {
				state.loading = false;
				state.error = null;
                state.features = action.payload;
			})
			.addCase(getProductFeatures.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			});
	},
});

export default productFeaturesSlice.reducer;
