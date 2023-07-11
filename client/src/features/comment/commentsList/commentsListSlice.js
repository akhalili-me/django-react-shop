import { createSlice } from "@reduxjs/toolkit";
import { getProductComments, getUserComments } from "./commentsListReducers";

export const commentsListSlice = createSlice({
  name: "commentsList",
  initialState: { comments: [], loading: null, error: null, count: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
		//Fetch product comments
      .addCase(getProductComments.pending, (state) => {
        state.loading = true;
      })
      .addCase(getUserComments.pending, (state) => {
        state.loading = true;
      })
      .addCase(getProductComments.fulfilled, (state, action) => {
        state.error = null;
        state.loading = false;
        state.comments = action.payload.results;
        state.count = action.payload.count;
      })

	  // Fetch user comments
      .addCase(getUserComments.fulfilled, (state, action) => {
        state.error = null;
        state.loading = false;
        state.comments = action.payload.results;
        state.count = action.payload.count;
      })
      .addCase(getProductComments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(getUserComments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default commentsListSlice.reducer;
