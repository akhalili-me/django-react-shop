import { createSlice } from "@reduxjs/toolkit";
import { getCommentById } from "./commentDetailsReducers";

export const commentDetailsSlice = createSlice({
	name: "commentDetails",
	initialState: { comment: {}, loading: null, error: null},
	reducers: {},
	extraReducers: (builder) => {
		builder
			// Fetch comment by id
			.addCase(getCommentById.pending, (state) => {
				state.loading = true;
			})
			.addCase(getCommentById.fulfilled, (state, action) => {
				state.loading = false;
                state.comment = action.payload
			})
			.addCase(getCommentById.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export default commentDetailsSlice.reducer;