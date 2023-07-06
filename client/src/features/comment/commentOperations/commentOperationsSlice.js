import { createSlice } from "@reduxjs/toolkit";
import {
	addComment,
	deleteComment,
	likeComment,
	deleteLikeComment,
} from "./commentOperationReducers";

export const commentOperationSlice = createSlice({
	name: "commentOperation",
	initialState: { loading: null, error: null, success: null },
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addMatcher(
				(action) =>
					[
						addComment.pending,
						deleteComment.pending,
						likeComment.pending,
						deleteLikeComment.pending,
					].includes(action.type),
				(state) => {
					state.loading = true;
					state.success = null;
				}
			)
			.addMatcher(
				(action) =>
					[
						addComment.fulfilled,
						deleteComment.fulfilled,
						likeComment.fulfilled,
						deleteLikeComment.fulfilled,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.success = true;
				}
			)
			.addMatcher(
				(action) =>
					[
						addComment.rejected,
						deleteComment.rejected,
						likeComment.rejected,
						deleteLikeComment.rejected,
					].includes(action.type),
				(state, action) => {
					state.loading = false;
					state.success = false;
					state.error = action.error.message;
				}
			);
	},
});

export default commentOperationSlice.reducer;
