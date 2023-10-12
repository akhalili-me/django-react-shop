import { createSlice } from "@reduxjs/toolkit";
import {
  addComment,
  likeComment,
  deleteLikeComment,
  updateComment,
} from "./commentOperationReducers";

export const commentOperationSlice = createSlice({
  name: "commentOperation",
  initialState: { loading: null, error: null, success: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Add comment
      .addCase(addComment.pending, (state,action) => {
        state.loading = true;
      })
      .addCase(addComment.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(addComment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Update comment
      .addCase(updateComment.pending, (state,action) => {
        state.loading = true;
        state.success = null;
        state.error = null;
      })
      .addCase(updateComment.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(updateComment.rejected, (state, action) => {
        state.loading = false;
        state.success = false;
        state.error = action.error.message;
      })

      // Like comment
      .addCase(likeComment.pending, (state,action) => {
        state.loading = true;
      })
      .addCase(likeComment.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(likeComment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })

      // Delete like comment
      .addCase(deleteLikeComment.pending, (state,action) => {
        state.loading = true;
      })
      .addCase(deleteLikeComment.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
        state.success = true;
      })
      .addCase(deleteLikeComment.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default commentOperationSlice.reducer;
