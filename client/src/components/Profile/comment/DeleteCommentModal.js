import React from "react";
import { Modal, Button } from "react-bootstrap";
import { deleteComment } from "../../../features/comment/commentOperations/commentOperationReducers";
import { useDispatch, useSelector } from "react-redux";
import { getUserComments } from "../../../features/comment/commentsList/commentsListReducers";
import { setAlarm } from "../../../features/alert/alarmSlice";
import Loader from "../../common/Loader";

const DeleteModal = ({ show, commentId, onClose }) => {
    const dispatch = useDispatch();

    const {loading,error,success} = useSelector(state => state.commentOperations)

    const handleSubmit = async (event) => {
        event.preventDefault();
        dispatch(deleteComment(commentId));

        if (success) {
            dispatch(getUserComments())
            dispatch(setAlarm({
                message: "Comment successfully deleted.",
                type: "success"
            }))
        }else if (success === false)
        {
            dispatch(
                setAlarm({
                    message: error,
                    type: "danger",
                })
            );
        }

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
                    {loading ? <Loader/> : "Delete"}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default DeleteModal;