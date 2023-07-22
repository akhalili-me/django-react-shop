import { createSlice } from "@reduxjs/toolkit";
import { getOrderById } from "./orderDetailsReducer";

export const orderDetailsSlice = createSlice({
	name: "orderDetails",
	initialState: { order: {}, loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch order by id
			.addCase(getOrderById.pending, (state) => {
				state.loading = true;
                state.error = null;
			})
			.addCase(getOrderById.fulfilled, (state, action) => {
				state.error = null;
				state.loading = false;
                state.order = action.payload
			})
			.addCase(getOrderById.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export default orderDetailsSlice.reducer;