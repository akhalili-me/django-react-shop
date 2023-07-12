import React from "react";
import { useDispatch } from "react-redux";
import { likeComment,deleteLikeComment } from "../../features/comment/commentOperations/commentOperationReducers";

const LikeComment = ({comment,productId,page}) => {
  const dispatch = useDispatch();

  const handleLikeComment = async () => {
    dispatch(likeComment({commentId: comment.id,productId,page}))
  };

  const handleDeleteLikeComment = async () => {
    dispatch(deleteLikeComment({commentId: comment.id,productId,page}))
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
