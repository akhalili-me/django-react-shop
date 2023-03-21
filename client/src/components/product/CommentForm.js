import React, { useState } from 'react'
import { Form , Row,Col,Button} from 'react-bootstrap'
import InputGroup from 'react-bootstrap/InputGroup';
import { addComment } from '../../utility/comment';
import {setAlarm} from '../../features/alert/alarmSlice'
import { useDispatch } from 'react-redux';

const CommentForm = ({productId,getComments}) => {
    const [rate,setRate] = useState(0);  
    const [comment,setComment] = useState('');  
    const dispatch = useDispatch()

    const clearFields = () => {
        setRate(0)
        setComment('')
    }

    const handleFieldChange = (event) => {
        const name = event.target.name
        const value = event.target.value

        switch (name) {
            case 'rate':
                setRate(value)
                break;
            case 'comment':
                setComment(value)
                break;
            default:
                break;
        }
    }

    const handleCommentSubmit = async (event) => {
        event.preventDefault();
        try {
            await addComment({text: comment,rate: rate},productId)
            getComments()
            dispatch(setAlarm({
                message: 'Comment Added Successfully',
                type: 'success',
                show: true
            }))
        } catch (error) {
            dispatch(setAlarm({
                message: error.message,
                type: 'danger',
                show: true
            }))
        } finally {
            clearFields()
        }
    }

  return (
    <Form onSubmit={handleCommentSubmit}>
        <Row>
            <Col md={8}>
                <InputGroup className="mb-3">
                    <InputGroup.Text>Review</InputGroup.Text>
                    <Form.Control as="textarea" rows={3} onChange={handleFieldChange} value={comment} name='comment' />
                </InputGroup>
            </Col>
            <Col md={4}>
                <InputGroup className="mb-3">
                    <InputGroup.Text><i class="fa-solid fa-star"></i></InputGroup.Text>
                    <Form.Select aria-label="Default select example" onChange={handleFieldChange} value={rate} name='rate'>
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
  )
}

export default CommentForm