import React, { useState } from "react";
import { likeComment, removeLikeComment } from "../../utility/comment";
import { useDispatch } from "react-redux";
import { setAlarm } from "../../features/alert/alarmSlice";

const LikeComment = ({ comment, getComments }) => {
  const dispatch = useDispatch();

  const handleLikeComment = async () => {
    try {
      await likeComment(comment.id);
      await getComments();

      dispatch(
        setAlarm({
          message: "Comment liked successfully",
          type: "success",
          show: true,
        })
      );
    } catch (error) {
      dispatch(
        setAlarm({
          message: error.message,
          type: "danger",
          show: true,
        })
      );
    }
  };

  const handleRemoveLikeComment = async () => {
    try {
      await removeLikeComment(comment.id);
      await getComments();

      dispatch(
        setAlarm({
          message: "Comment like removed successfully",
          type: "success",
          show: true,
        })
      );
    } catch (error) {
      dispatch(
        setAlarm({
          message: error.message,
          type: "danger",
          show: true,
        })
      );
    }
  };

  return (
    <>
      <span> {comment.likes} </span>
      {comment.liked_by_current_user ? (
        <i onClick={handleRemoveLikeComment} class="fa-solid fa-thumbs-up"></i>
      ) : (
        <i onClick={handleLikeComment} class="fa-regular fa-thumbs-up"></i>
      )}
    </>
  );
};

export default LikeComment;
