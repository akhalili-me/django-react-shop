import authAxios from "../../../utility/api";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getProductComments = createAsyncThunk(
  "comments/productComments",
  async ({productId,page}) => {
    try {
      const { data } = await authAxios.get(`/products/${productId}/comments?page=${page}`);
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

export const getUserComments = createAsyncThunk(
  "comments/userComments",
  async () => {
    try {
      const { data } = await authAxios.get("/accounts/comments");
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

