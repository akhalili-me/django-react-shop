import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getUserOrders = createAsyncThunk(
  "order/orderList",
  async () => {
    try {
      const { data } = await authAxios.get(`/cart/orders`);
      return data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
    }
  }
);


