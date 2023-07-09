import authAxios from "../../../utility/api";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getUserAddresses = createAsyncThunk(
  "addressList/userAddresses",
  async () => {
    try {
      const { data } = await authAxios.get(`/accounts/address`);
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

