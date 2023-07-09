import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getAddressById = createAsyncThunk(
  "addressDetails/addressById",
  async (addressId) => {
    try {
      const { data } = await authAxios.get(`/accounts/address/${addressId}`);
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

