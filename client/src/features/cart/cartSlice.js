import { createSlice } from "@reduxjs/toolkit";
import {
  addItemReducer,
  removeItemReducer,
  UpdateItemQuantityReducer,
  clearAllItmesReducer,
} from "./cartReducers";
import { getCartItems } from "./cartOperations";

export const cartSlice = createSlice({
  name: "cart",
  initialState: { total: 0, items: [] },
  reducers: {
    addItemCart: addItemReducer,
    removeItemCart: removeItemReducer,
    updateItemCart: UpdateItemQuantityReducer,
    clearCart: clearAllItmesReducer,
  },
  extraReducers: (builder) => {
    builder.addCase(getCartItems.fulfilled, (state, action) => {
      state.total = action.payload.total;
      state.items = action.payload.cart_items;
    });
  },
});

// Action creators are generated for each case reducer function
export const { addItemCart, removeItemCart, updateItemCart, clearCart } = cartSlice.actions;

export default cartSlice.reducer;
