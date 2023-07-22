import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getOrderById = createAsyncThunk(
  "orderDetails/orderById",
  async ({orderId}) => {
    try {
      const { data } = await authAxios.get(`/cart/orders/${orderId}`);
      return data;
    } catch (error) {
      const errorMessage =
        error.response && error.response.data.detail
          ? error.response.data.detail
          : error.message;
      throw new Error(errorMessage);
    }
  }
);

