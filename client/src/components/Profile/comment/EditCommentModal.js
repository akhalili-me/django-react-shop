import React, { useEffect, useState } from "react";
import { Modal, InputGroup, Form, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { getCommentById } from "../../../features/comment/commentDetails/commentDetailsReducers";
import { updateComment } from "../../../features/comment/commentOperations/commentOperationReducers";
import { getUserComments } from "../../../features/comment/commentsList/commentsListReducers";

const EditModal = ({ show, commentId, onClose }) => {
    const dispatch = useDispatch();
    const [text, setText] = useState("");
    const [rate, setRate] = useState(0);
    const { loading,comment } = useSelector((state) => state.commentDetails);
    const { success, error } = useSelector((state) => state.commentOperations);

    useEffect(() => {
        if (commentId !== 0) {
            dispatch(getCommentById(commentId));
            setText(comment.text);
            setRate(comment.rate);
        }
    }, [commentId, dispatch]);

    const handleSubmit = async () => {
        dispatch(updateComment({ commentId, text, rate }));

        if (success) {
            dispatch(getUserComments());
            dispatch(
                setAlarm({
                    message: "Comment successfully updated.",
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
        <Modal show={show} onHide={onClose}>
            <Modal.Header closeButton>
                <Modal.Title>Edit Comment</Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <InputGroup className="mb-3">
                    <InputGroup.Text>Comment</InputGroup.Text>
                    <Form.Control
                        as="textarea"
                        rows={3}
                        name="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />
                </InputGroup>
                <InputGroup className="mb-3">
                    <InputGroup.Text>
                        <i class="fa-solid fa-star"></i>
                    </InputGroup.Text>
                    <Form.Select
                        aria-label="Default select example"
                        name="rate"
                        value={rate}
                        onChange={(e) => setRate(e.target.value)}
                    >
                        <option>Rate</option>
                        <option value={1}>1</option>
                        <option value={2}>2</option>
                        <option value={3}>3</option>
                        <option value={4}>4</option>
                        <option value={5}>5</option>
                    </Form.Select>
                </InputGroup>
            </Modal.Body>

            <Modal.Footer>
                <Button variant="secondary" onClick={onClose}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSubmit} disabled={loading}>
                    Submit
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default EditModal;
