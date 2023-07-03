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
    CART_ADD_ITEM: addItemReducer,
    CART_REMOVE_ITEM: removeItemReducer,
    CART_UPDATE_ITEM: UpdateItemQuantityReducer,
    CART_CLEAR_CART: clearAllItmesReducer,
  },
  extraReducers: (builder) => {
    builder.addCase(fetchCartItems.fulfilled, (state, action) => {
      state.total = action.payload[0].total;
      state.items = action.payload[0].cart_items;
    });
  },
});

// Action creators are generated for each case reducer function
export const { CART_ADD_ITEM, CART_REMOVE_ITEM, CART_UPDATE_ITEM, CART_CLEAR_CART } = cartSlice.actions;

export default cartSlice.reducer;
