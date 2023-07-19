import { createSlice } from "@reduxjs/toolkit";
import { getUserOrders } from "./orderListReducers";

export const orderListSlice = createSlice({
	name: "orderList",
	initialState: { orders: [], loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch top sold products of child category by parent category id
			.addCase(getUserOrders.pending, (state) => {
				state.loading = true;
			})
			.addCase(getUserOrders.fulfilled, (state, action) => {
				state.loading = false;
				state.error = null;
                state.orders = action.payload
			})
			.addCase(getUserOrders.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export default orderListSlice.reducer;
