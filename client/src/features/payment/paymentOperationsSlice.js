import { createSlice } from "@reduxjs/toolkit";
import { paymentFailed, paymentSuccessfull } from "./paymentOperationsReducer";

export const paymentOperationSlice = createSlice({
  name: "orderOperations",
  initialState: { loading: null, error: null, success: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Submit successfull payment
      .addCase(paymentSuccessfull.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(paymentSuccessfull.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(paymentSuccessfull.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Submit failed payment
      .addCase(paymentFailed.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(paymentFailed.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(paymentFailed.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default paymentOperationSlice.reducer;
