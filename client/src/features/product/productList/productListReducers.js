import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getProductsByFilter = createAsyncThunk(
  "product/filterProducts",
  async ({ childCategoryId, params }) => {
    try {
      const URL = `/products/filter/${childCategoryId}?${params}`;
      const { data } = await authAxios.get(URL);
      return data;
    } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);

export const getProductsByNameSearch = createAsyncThunk(
  "product/searchProducts",
  async ({ q }) => {
    try {
      const URL = `/products/search/${q}`;
      const { data } = await authAxios.get(URL);
      return data;
    } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);

