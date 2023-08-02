import { createSlice } from "@reduxjs/toolkit";
import { getCartItems } from "./cartOperations";
import {
  addItemToCart,
  addItemToState,
  removeItemFromCart,
  removeItemFromState,
  UpdateItemQuantityInCart,
  UpdateItemQuantityInState,
  clearAllItmesInCart,
} from "./cartReducers";

export const cartSlice = createSlice({
  name: "cart",
  initialState: { total: 0, items: [] },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getCartItems.fulfilled, (state, action) => {
      state.total = action.payload.total;
      state.items = action.payload.cart_items;
    });
    builder.addCase(addItemToCart.fulfilled, (state, action) => {
      addItemToState(state, action.payload);
    });
    builder.addCase(removeItemFromCart.fulfilled, (state, action) => {
      removeItemFromState(state, action.payload);
    });
    builder.addCase(UpdateItemQuantityInCart.fulfilled, (state, action) => {
      UpdateItemQuantityInState(state, action.payload);
    });
    builder.addCase(clearAllItmesInCart.fulfilled, (state, action) => {
      state.total = 0;
      state.items = [];
    });
  },
});

export default cartSlice.reducer;
