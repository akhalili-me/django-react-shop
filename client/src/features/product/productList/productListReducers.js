import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getLatestProducts = createAsyncThunk(
  "product/latestProducts",
  async () => {
    try {
      const { data } = await authAxios.get("/products/");
      return data;
    } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);

export const getProductsByFilter = createAsyncThunk(
  "product/filterProducts",
  async ({ childCategoryId, params }) => {
    try {
      const URL = `/products/search/${childCategoryId}?${params}`;
      const { data } = await authAxios.get(URL);
      return data;
    } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);

export const getChildCategoriesWithTopSoldProducts = createAsyncThunk(
  "product/filterProducts",
  async (childCategoryId, urlParams) => {
    try {
      const URL = `/products/search/${childCategoryId}?${urlParams}`;
      const { data } = authAxios.get(URL);
      return data;
    } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);
