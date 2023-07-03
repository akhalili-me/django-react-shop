import { createSlice } from "@reduxjs/toolkit";
import {
  addItemReducer,
  removeItemReducer,
  UpdateItemQuantityReducer,
  clearAllItmesReducer,
} from "./cartReducers";
import authAxios from "../../utility/api";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const fetchCartItems = createAsyncThunk(
  "cart/fetchCartItems",
  async () => {
    const response = await authAxios.get("/cart");
    return response.data;
  }
);

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
    builder.addCase(fetchCartItems.fulfilled, (state, action) => {
      state.total = action.payload[0].total;
      state.items = action.payload[0].cart_items;
    });
  },
});

// Action creators are generated for each case reducer function
export const { addItemCart, removeItemCart, updateItemCart, clearCart } = cartSlice.actions;

export default cartSlice.reducer;
