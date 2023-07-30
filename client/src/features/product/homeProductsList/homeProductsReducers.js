import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getNewestProducts = createAsyncThunk(
  "homeProductList/newestProducts",
  async () => {
    try {
      const { data } = await authAxios.get(`/products?sort=newest`);
      return data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
    }
  }
);
export const getBestSellingProducts = createAsyncThunk(
  "homeProductList/bestSellingProducts",
  async () => {
    try {
      const { data } = await authAxios.get(`/products?sort=bestselling`);
      return data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
    }
  }
);
export const getMostViewedProducts = createAsyncThunk(
  "homeProductList/mostViewedProducts",
  async () => {
    try {
      const { data } = await authAxios.get(`/products?sort=most_viewed`);
      return data;
    } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
    }
  }
);


