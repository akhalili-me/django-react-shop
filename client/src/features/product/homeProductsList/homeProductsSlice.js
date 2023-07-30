import { createSlice } from "@reduxjs/toolkit";
import {
  getNewestProducts,
  getBestSellingProducts,
  getMostViewedProducts,
} from "./homeProductsReducers";

export const homeProducts = createSlice({
  name: "homeProducts",
  initialState: { newest: {}, bestselling: {}, mostViewed: {} },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch newest added products
      .addCase(getNewestProducts.pending, (state) => {
        state.newest.loading = true;
      })
      .addCase(getNewestProducts.fulfilled, (state, action) => {
        state.newest.loading = false;
        state.newest.error = null;
        state.newest.products = action.payload;
      })
      .addCase(getNewestProducts.rejected, (state, action) => {
        state.newest.loading = false;
        state.newest.error = action.error.message;
      })

      //   fetch bestselling products
      .addCase(getBestSellingProducts.pending, (state) => {
        state.bestselling.loading = true;
      })
      .addCase(getBestSellingProducts.fulfilled, (state, action) => {
        state.bestselling.loading = false;
        state.bestselling.error = null;
        state.bestselling.products = action.payload;
      })
      .addCase(getBestSellingProducts.rejected, (state, action) => {
        state.bestselling.loading = false;
        state.bestselling.error = action.error.message;
      })

      // fetch most viewed products
      .addCase(getMostViewedProducts.pending, (state) => {
        state.mostViewed.loading = true;
      })
      .addCase(getMostViewedProducts.fulfilled, (state, action) => {
        state.mostViewed.loading = false;
        state.mostViewed.error = null;
        state.mostViewed.products = action.payload;
      })
      .addCase(getMostViewedProducts.rejected, (state, action) => {
        state.mostViewed.loading = false;
        state.mostViewed.error = action.error.message;
      });
  },
});

export default homeProducts.reducer;
