import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getChildCategoriesWithTopSoldProducts = createAsyncThunk(
  "productList/childCategoryProducts",
  async ({parentCategoryId}) => {
    try {
      const { data } = await authAxios.get(`/products/category/${parentCategoryId}`);
      return data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
    }
  }
);


