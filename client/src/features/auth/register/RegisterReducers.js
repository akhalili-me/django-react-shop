import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";
import { jsonErrorstoString } from "../../../utility/string_utils";

export const register = createAsyncThunk(
  "auth/register",
  async ({ email, username, password }) => {
    try {
      const { data } = await authAxios.post("/accounts/register", {
        email,
        username,
        password,
      });
      return data;
    } catch (error) {
      const errorMessage = jsonErrorstoString(error.response?.data) || error.message
      throw new Error(errorMessage);
    }
  }
);

export const clearRegisterErrorsReducers = (state, action) => {
  state.error = null;
};
