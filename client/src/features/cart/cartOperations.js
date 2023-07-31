import authAxios from "../../utility/api";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getCartItems = createAsyncThunk("cart/getCartItems", async () => {
  try {
    const { data } = await authAxios.get("/cart");
    return data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message;
    throw new Error(errorMessage);
  }
});

export const removeAllItemsInDatabase = async () => {
  try {
    await authAxios.delete("/cart/removeall");
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message;
    throw new Error(errorMessage);
  }
};

export const removeItemInDatabase = async (id) => {
  try {
    await authAxios.delete(`/cart/${id}`);
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message;
    throw new Error(errorMessage);
  }
};

export const addOrUpdateItemInDatabase = async (id, quantity) => {
  try {
    await authAxios.post("/cart/create", {
      product: id,
      quantity: quantity,
    });
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message;
    throw new Error(errorMessage);
  }
};
