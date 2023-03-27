import React, { useState, useEffect } from "react";
import { Button, Row, Col, ListGroup, ButtonGroup } from "react-bootstrap";
import { fetchUserComments, DeleteComment } from "../../utility/comment";
import { useDispatch } from "react-redux";
import DeleteModal from "../common/DeleteModal";
import Rating from "../common/Rating";
import { setAlarm } from "../../features/alert/alarmSlice";
import EditModal from "./EditCommentModal";

const Comments = () => {
  const dispatch = useDispatch();
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [comments, setComments] = useState([]);
  const [commentId, setCommentId] = useState(0);

  useEffect(() => {
    const getComments = async () => {
      const { data } = await await fetchUserComments();
      setComments(data);
    };

    getComments();
  }, []);

  const handleShowModal = async (event) => {
    const { name, dataset } = event.target;
    const id = parseInt(dataset.commentid);

    if (name === "delete") {
      setShowDeleteModal(true);
    } else if (name === "edit") {
      setShowEditModal(true);
    }

    setCommentId(id);
  };

  const handleCloseModal = () => {
    setShowDeleteModal(false);
    setShowEditModal(false);
  };

  const deleteComment = async () => {
    try {
      await DeleteComment(commentId);
      const updatedComments = comments.filter(
        (comment) => comment.id !== commentId
      );
      setComments(updatedComments);
      dispatch(
        setAlarm({
          message: "Comment deleted successfully",
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
    } finally {
      setShowDeleteModal(false);
    }
  };

  const updateCommentState = (comment) => {
    const updatedCommentIndex = comments.findIndex((c) => c.id === comment.id);
    comments[updatedCommentIndex] = comment;
    setComments(comments);
  };

  return (
    <>
      <DeleteModal
        show={showDeleteModal}
        onSubmit={deleteComment}
        onClose={handleCloseModal}
        message={"Are you sure to delete this comment?"}
      />
      <EditModal
        show={showEditModal}
        onClose={handleCloseModal}
        commentId={commentId}
        updateCommentState={updateCommentState}
      />

      <ListGroup>
        {comments.map((comment) => (
          <ListGroup.Item key={comment.id}>
            <Row>
              <Col md={10}>
                <p>{comment.text}</p>
                <Rating
                  value={comment.rate}
                  text={
                    <>
                      {comment.likes} <i class="fa-solid fa-thumbs-up"></i>
                    </>
                  }
                />
              </Col>
              <Col md={2}>
                <ButtonGroup className="comment_buttons">
                  <Button
                    onClick={handleShowModal}
                    data-commentid={comment.id}
                    name="edit"
                    variant="warning"
                  >
                    <i
                      class="fas fa-edit"
                      style={{ pointerEvents: "none" }}
                    ></i>
                  </Button>
                  <Button
                    onClick={handleShowModal}
                    data-commentid={comment.id}
                    name="delete"
                    variant="danger"
                  >
                    <i
                      className="fas fa-trash"
                      style={{ pointerEvents: "none" }}
                    ></i>
                  </Button>
                </ButtonGroup>
              </Col>
            </Row>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </>
  );
};

export default Comments;
