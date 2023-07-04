import axios from "axios";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getProductDetails = createAsyncThunk(
  "productDetails/getProductDetails",
  async (productId) => {
    try {
      const { data } = await axios.get(`/products/${productId}/`);
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

