import React, { useState, useEffect } from "react";
import { Button, Row, Col, ListGroup, ButtonGroup } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import DeleteModal from "../../common/DeleteModal";
import Rating from "../../common/Rating";
import EditModal from "./EditCommentModal";
import { Link } from "react-router-dom";
import { getUserComments } from "../../../features/comment/commentsList/commentsListReducers";
import Loader from "../../common/Loader";
import Message from "../../common/Message";
import DeleteCommentModal from "./DeleteCommentModal";

const Comments = () => {
    const dispatch = useDispatch();
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [commentId, setCommentId] = useState(0);

    const { comments, loading, error } = useSelector(
        (state) => state.commentList
    );

    useEffect(() => {
        dispatch(getUserComments());
    }, [dispatch]);

    return (
        <>
            <DeleteCommentModal
                show={showDeleteModal}
                onClose={() => setShowDeleteModal(false)}
                commentId={commentId}
            />

            <EditModal
                show={showEditModal}
                onClose={() => setShowEditModal(false)}
                commentId={commentId}
            />

            <ListGroup>
                {loading ? (
                    <Loader />
                ) : error ? (
                    <Message variant={"danger"} message={error} />
                ) : (
                    comments?.map((comment) => (
                        <ListGroup.Item key={comment.id}>
                            <Row>
                                <Col md={10}>
                                    <p>{comment.text}</p>
                                    <Rating
                                        value={comment.rate}
                                        text={
                                            <>
                                                {comment.likes}{" "}
                                                <i class="fa-solid fa-thumbs-up"></i>
                                            </>
                                        }
                                    />
                                </Col>
                                <Col md={2}>
                                    <ButtonGroup className="comment_buttons">
                                        <Button
                                            onClick={() => {
                                                setCommentId(comment.id);
                                                setShowEditModal(true);
                                            }}
                                            name="edit"
                                            variant="warning"
                                        >
                                            <i
                                                class="fas fa-edit"
                                                style={{
                                                    pointerEvents: "none",
                                                }}
                                            ></i>
                                        </Button>
                                        <Button
                                            onClick={() => {
                                                setCommentId(comment.id);
                                                setShowDeleteModal(true);
                                            }}
                                            name="delete"
                                            variant="danger"
                                        >
                                            <i
                                                className="fas fa-trash"
                                                style={{
                                                    pointerEvents: "none",
                                                }}
                                            ></i>
                                        </Button>
                                    </ButtonGroup>
                                </Col>
                            </Row>
                            <Link to={`/product/${comment.product?.id}`}>
                                <div className="mt-2">
                                    <strong>Product:</strong>{" "}
                                    {comment.product?.name}
                                </div>
                            </Link>
                        </ListGroup.Item>
                    ))
                )}
            </ListGroup>
        </>
    );
};

export default Comments;
