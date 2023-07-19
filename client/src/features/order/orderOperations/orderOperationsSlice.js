import { createSlice } from "@reduxjs/toolkit";
import {
  addOrder,
  updateOrder,
  deleteOrder,
  deleteOrderItem,
  updateOrderItem,
  deleteOrderPayment,
  updateOrderPayment,
} from "./orderOperationsReducers";

export const orderOperationsSlice = createSlice({
  name: "orderOperations",
  initialState: { loading: null, error: null, success: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Add order
      .addCase(addOrder.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(addOrder.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(addOrder.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Update order
      .addCase(updateOrder.pending, (state, action) => {
        state.loading = true;
        state.success = null;
        state.error = null;
      })
      .addCase(updateOrder.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(updateOrder.rejected, (state, action) => {
        state.loading = false;
        state.success = false;
        state.error = action.error.message;
      })

      // Delete order
      .addCase(deleteOrder.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(deleteOrder.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(deleteOrder.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Delete order item
      .addCase(deleteOrderItem.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(deleteOrderItem.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(deleteOrderItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Update order item
      .addCase(updateOrderItem.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(updateOrderItem.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(updateOrderItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Delete order payment
      .addCase(deleteOrderPayment.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(deleteOrderPayment.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(deleteOrderPayment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Update order payment
      .addCase(updateOrderPayment.pending, (state, action) => {
        state.loading = true;
      })
      .addCase(updateOrderPayment.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(updateOrderPayment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default orderOperationsSlice.reducer;
