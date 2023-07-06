import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const addComment = createAsyncThunk(
	"commentOperations/addComment",
	async ({ comment, productId }) => {
		try {
			await authAxios.post(`/products/${productId}/comments/create`, {
				text: comment.text,
				rate: comment.rate,
			});
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const updateComment = createAsyncThunk(
	"commentOperations/addComment",
	async ({commentId,text,rate}) => {
		try {
      await authAxios.put(`/accounts/comments/${commentId}`, {
        text: text,
        rate: rate,
      });
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const deleteComment = createAsyncThunk(
	"commentOperations/addComment",
	async (commentId) => {
		try {
      await authAxios.delete(`/accounts/comments/${commentId}`);
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const likeComment = createAsyncThunk(
	"commentOperations/likeComment",
	async (commentId) => {
		try {
      await authAxios.post(`/accounts/comments/${commentId}/like/`);
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const deleteLikeComment = createAsyncThunk(
	"commentOperations/deleteLikeComment",
	async (commentId) => {
		try {
      await authAxios.delete(`/accounts/comments/${commentId}/like/remove`);
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);