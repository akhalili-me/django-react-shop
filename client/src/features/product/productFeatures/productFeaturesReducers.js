import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getProductFeatures = createAsyncThunk(
  "product/productFeatures",
  async ({productId}) => {
    try {
      const { data } = await authAxios.get(`/products/${productId}/features`);
      return data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
    }
  }
);


