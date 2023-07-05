import { createSlice } from "@reduxjs/toolkit";
import { getProductComments, getUserComments } from "./commentsListReducers";

export const commentsListSlice = createSlice({
	name: "commentsList",
	initialState: { comments: [], loading: null, error: null, count: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addMatcher(
				(action) =>
					[
						getProductComments.pending,
						getUserComments.pending,
					].includes(action.type),
				(state) => {
					state.loading = true;
				}
			)
			.addMatcher(
				(action) =>
					[
						getProductComments.fulfilled,
						getUserComments.fulfilled,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.comments = action.payload.results;
					state.count = action.payload.count;
				}
			)
			.addMatcher(
				(action) =>
					[
						getProductComments.rejected,
						getUserComments.rejected,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.error = action.error.message;
				}
			);
	},
});

export default commentsListSlice.reducer;
