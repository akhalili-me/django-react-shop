import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";
import { setAlarm } from "../../alert/alarmSlice";
import { getUserComments,getProductComments } from "../commentsList/commentsListReducers";

export const addComment = createAsyncThunk(
    "commentOperations/addComment",
    async ({ comment, productId },{dispatch}) => {
        try {

            await authAxios.post(`/products/${productId}/comments/create`, {
                text: comment.text,
                rate: comment.rate,
            });

			dispatch(
                setAlarm({
                    message: "Comment successfully added.",
                    type: "success",
                })
            );
			dispatch(getProductComments({productId,page: 1}))
        } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
			dispatch(setAlarm({ message: errorMessage, type: "danger" }));
            throw new Error(errorMessage);
        }
    }
);

export const updateComment = createAsyncThunk(
    "commentOperations/updateComment",
    async ({ commentId, text, rate }, { dispatch }) => {
        try {
            await authAxios.patch(`/accounts/comments/${commentId}`, {
                text: text,
                rate: rate,
            });
            dispatch(
                setAlarm({
                    message: "Comment successfully updated.",
                    type: "success",
                })
            );
            dispatch(getUserComments());
        } catch (error) {
 			const errorMessage = error.response?.data?.detail || error.message;
            dispatch(setAlarm({ message: errorMessage, type: "danger" }));
            throw new Error(errorMessage);
        }
    }
);

export const deleteComment = createAsyncThunk(
    "commentOperations/deleteComment",
    async (commentId,{dispatch}) => {
        try {
            await authAxios.delete(`/accounts/comments/${commentId}`);

            dispatch(
                setAlarm({
                    message: "Comment successfully deleted.",
                    type: "success",
                })
            );
            dispatch(getUserComments());

        } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
			dispatch(setAlarm({ message: errorMessage, type: "danger" }));
            throw new Error(errorMessage);
        }
    }
);

export const likeComment = createAsyncThunk(
    "commentOperations/likeComment",
    async ({commentId,productId,page},{dispatch}) => {
        try {
            await authAxios.post(`/products/commentlike/create/${commentId}`);

			dispatch(
                setAlarm({
                    message: "Comment like successfully added.",
                    type: "success",
                })
            );
            dispatch(getProductComments({productId,page}));
        } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
			dispatch(setAlarm({ message: errorMessage, type: "danger" }));
            throw new Error(errorMessage);
        }
    }
);

export const deleteLikeComment = createAsyncThunk(
    "commentOperations/deleteLikeComment",
    async ({commentId,productId,page},{dispatch}) => {
        try {
            await authAxios.delete(
                `/products/commentlike/remove/${commentId}`
            );

			dispatch(
                setAlarm({
                    message: "Comment like successfully removed.",
                    type: "success",
                })
            );
            dispatch(getProductComments({productId,page}));
        } catch (error) {
			const errorMessage = error.response?.data?.detail || error.message;
			dispatch(setAlarm({ message: errorMessage, type: "danger" }));
            throw new Error(errorMessage);
        }
    }
);
