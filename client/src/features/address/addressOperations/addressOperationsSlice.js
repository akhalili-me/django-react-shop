import { createSlice } from "@reduxjs/toolkit";
import {
  addAddress,
  updateAddress,
  deleteAddress,
} from "./addressOperationsReducers";

export const addressOperationsSlice = createSlice({
  name: "AddressOperations",
  initialState: { loading: null, error: null, success: null },
  reducers: {},
  extraReducers: (builder) => {
    builder

      // Add address
      .addCase(addAddress.pending, (state) => {
        state.error = null;
        state.loading = true;
      })
      .addCase(addAddress.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(addAddress.rejected, (state, action) => {
        state.loading = false;
        state.success = false;
        state.error = action.error.message;
      })

      // Update address
      .addCase(updateAddress.pending, (state) => {
        state.error = null;
        state.loading = true;
      })
      .addCase(updateAddress.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(updateAddress.rejected, (state, action) => {
        state.loading = false;
        state.success = false;
        state.error = action.error.message;
      })

      // Delete address
      .addCase(deleteAddress.pending, (state) => {
        state.error = null;
        state.loading = true;
      })
      .addCase(deleteAddress.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(deleteAddress.rejected, (state, action) => {
        state.loading = false;
        state.success = false;
        state.error = action.error.message;
      })
    
  },
});

export default addressOperationsSlice.reducer;
