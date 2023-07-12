import React, { useState } from "react";
import { Form, Row, Col, Button } from "react-bootstrap";
import InputGroup from "react-bootstrap/InputGroup";
import { setAlarm } from "../../features/alert/alarmSlice";
import { useDispatch, useSelector } from "react-redux";
import { getProductComments } from "../../features/comment/commentsList/commentsListReducers";
import { addComment } from "../../features/comment/commentOperations/commentOperationReducers";

const CommentForm = ({ productId }) => {
  const [rate, setRate] = useState(0);
  const [text, setText] = useState("");
  const dispatch = useDispatch();

  const clearFields = () => {
    setRate(0);
    setText("");
  };

  const handleCommentSubmit = async (event) => {
    event.preventDefault();
    const comment = { text: text, rate: rate }
    dispatch(addComment({comment,productId}))
    clearFields()
  };

  return (
    <Form onSubmit={handleCommentSubmit}>
      <Row>
        <Col md={8}>
          <InputGroup className="mb-3">
            <InputGroup.Text>Review</InputGroup.Text>
            <Form.Control
              as="textarea"
              rows={3}
              onChange={(e) => setText(e.target.value)}
              value={text}
              name="text"
            />
          </InputGroup>
        </Col>
        <Col md={4}>
          <InputGroup className="mb-3">
            <InputGroup.Text>
              <i class="fa-solid fa-star"></i>
            </InputGroup.Text>
            <Form.Select
              aria-label="Default select example"
              onChange={(e) => setRate(e.target.value)}
              value={rate}
              name="rate"
            >
              <option>Rate</option>
              <option value={1}>1</option>
              <option value={2}>2</option>
              <option value={3}>3</option>
              <option value={4}>4</option>
              <option value={5}>5</option>
            </Form.Select>
          </InputGroup>
          <Button variant="primary" type="submit" className="col-12">
            Submit Comment
          </Button>
        </Col>
      </Row>
    </Form>
  );
};

export default CommentForm;
