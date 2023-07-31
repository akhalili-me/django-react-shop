import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const getCommentById = createAsyncThunk(
  "commentDetails/commentById",
  async (commentId) => {
    try {
      const { data } = await authAxios.get(`/accounts/comments/${commentId}`);
      return data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);

