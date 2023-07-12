import React, { useEffect, useState } from "react";
import { Modal, Button } from "react-bootstrap";
import { deleteComment } from "../../../features/comment/commentOperations/commentOperationReducers";
import { useDispatch, useSelector } from "react-redux";
import { getUserComments } from "../../../features/comment/commentsList/commentsListReducers";
import { setAlarm } from "../../../features/alert/alarmSlice";
import Loader from "../../common/Loader";

const DeleteCommentModal = ({ show, commentId, onClose }) => {
  const dispatch = useDispatch();

  const { loading } = useSelector((state) => state.commentOperations);

  const handleSubmit = (event) => {
    dispatch(deleteComment(commentId));
    onClose();
  };

  return (
    <Modal show={show} onHide={onClose}>
      <Modal.Header closeButton>
        <Modal.Title>Delete</Modal.Title>
      </Modal.Header>
      <Modal.Body>Are you sure to delete this comment?</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onClose}>
          Close
        </Button>
        <Button variant="danger" onClick={handleSubmit}>
          {loading ? <Loader /> : "Delete"}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default DeleteCommentModal;
