import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { setAlarm } from "../../features/alert/alarmSlice";
import { likeComment,deleteLikeComment } from "../../features/comment/commentOperations/commentOperationReducers";
import { getProductComments } from "../../features/comment/commentsList/commentsListReducers";

const LikeComment = ({comment,commentId}) => {
  const dispatch = useDispatch();
  const { success, error } = useSelector(
      (state) => state.commentOperations
  );

  const handleLikeComment = async () => {
    dispatch(likeComment(comment.id))

    if (success) {
      dispatch(getProductComments(commentId))
      dispatch(
        setAlarm({
            message: "Comment liked successfully",
            type: "success",
        })
    );
    } else if (success === false) {
      dispatch(
        setAlarm({
            message: error,
            type: "danger",
        })
    );
    }
  };

  const handleDeleteLikeComment = async () => {
    dispatch(deleteLikeComment(comment.id))
    if (success) {
      dispatch(getProductComments(commentId))
      dispatch(
        setAlarm({
            message: "Comment like removed successfully.",
            type: "success",
        })
    );
    } else if (success === false) {
      dispatch(
        setAlarm({
            message: error,
            type: "danger",
        })
    );
    }
  };

  return (
    <>
      <span> {comment.likes} </span>
      {comment.liked_by_current_user ? (
        <i onClick={handleDeleteLikeComment} class="fa-solid fa-thumbs-up"></i>
      ) : (
        <i onClick={handleLikeComment} class="fa-regular fa-thumbs-up"></i>
      )}
    </>
  );
};

export default LikeComment;
