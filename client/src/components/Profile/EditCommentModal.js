import React,{useEffect,useState} from 'react'
import { Modal,InputGroup,Form,Button } from 'react-bootstrap'
import { useDispatch } from 'react-redux'
import { setAlarm } from '../../features/alert/alarmSlice'
import { retrieveComment,updateComment } from '../../utility/comment'


const EditModal = ({show,commentId,onClose,updateCommentState}) => {
    const dispatch = useDispatch()
    const [comment,setComment] = useState({})
   

    useEffect(() => {
        const getComment = async () => {
            const {data} = await retrieveComment(commentId)
            setComment(data)
        }

        if (commentId !== 0) {
            getComment()
        }
    },[commentId])

    const handleClose = () => {
        onClose()
    };

    const handleSubmit = async () => {
      try {
          await updateComment(comment)
          updateCommentState(comment)
          dispatch(setAlarm({
              message: 'Comment edited successfully',
              type: 'success',
              show: true
        }))
      } 
      catch (error) {
            dispatch(setAlarm({
            message: error.message,
            type: 'danger',
            show: true
          }))
      }
      handleClose()
    }

    const handleFieldChange = (event) => {
        setComment({
          ...comment,
          [event.target.name]: event.target.value
        });
    };

    return (
      <Modal show={show} onHide={handleClose} >
        <Modal.Header closeButton>
          <Modal.Title>Edit Comment</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <InputGroup className="mb-3">
            <InputGroup.Text>Comment</InputGroup.Text>
            <Form.Control as="textarea" rows={3}  name='text' value={comment.text} onChange={handleFieldChange}/>
          </InputGroup>
          <InputGroup className="mb-3">
            <InputGroup.Text><i class="fa-solid fa-star"></i></InputGroup.Text>
            <Form.Select aria-label="Default select example" name='rate' value={comment.rate} onChange={handleFieldChange}>
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

          <Button variant="secondary" onClick={handleClose}>
              Close
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
              Submit
          </Button>

        </Modal.Footer>
    </Modal>
  )
}

export default EditModal