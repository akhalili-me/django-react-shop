import React, { useEffect, useState } from "react";
import { Modal, InputGroup, Form, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { getCommentById } from "../../../features/comment/commentDetails/commentDetailsReducers";
import { updateComment } from "../../../features/comment/commentOperations/commentOperationReducers";
import Loader from "../../common/Loader";
import Message from "../../common/Message";

const EditCommentModal = ({ show, commentId, onClose }) => {
  const dispatch = useDispatch();
  const [formData, setFormData] = useState({ text: "", rate: 0 });
  const commentDetails = useSelector((state) => state.commentDetails);
  const { comment } = commentDetails;

  useEffect(() => {
    if (commentId !== 0) {
      dispatch(getCommentById(commentId));
    }
  }, [commentId, dispatch]);

  useEffect(() => {
    if (comment) {
      setFormData({ text: comment.text, rate: comment.rate });
    }
  }, [comment]);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (commentId && formData.text && formData.rate) {
      dispatch(updateComment({ commentId, ...formData }));
    } else {
      setAlarm({
        message: "Please fill in all the required fields.",
        type: "danger",
      });
    }
    onClose();
  };

  return (
    <Modal show={show} onHide={onClose}>
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Comment</Modal.Title>
        </Modal.Header>
        {commentDetails.loading ? (
          <Loader />
        ) : commentDetails.error ? (
          <Message variant={"danger"} message={commentDetails.error} />
        ) : (
          <Modal.Body>
            <InputGroup className="mb-3">
              <InputGroup.Text>Comment</InputGroup.Text>
              <Form.Control
                as="textarea"
                rows={3}
                name="text"
                value={formData.text}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    text: e.target.value,
                  })
                }
              />
            </InputGroup>
            <InputGroup className="mb-3">
              <InputGroup.Text>
                <i className="fa-solid fa-star"></i>
              </InputGroup.Text>
              <Form.Select
                aria-label="Default select example"
                name="rate"
                value={formData.rate}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    rate: e.target.value,
                  })
                }
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
        )}

        <Modal.Footer>
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
          <Button
            variant="primary"
            disabled={commentDetails.loading === true}
            type="submit"
          >
            Submit
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default EditCommentModal;
