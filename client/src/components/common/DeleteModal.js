import React from "react";
import { Modal, Button } from "react-bootstrap";

const DeleteModal = ({ show, message, onClose, onSubmit }) => {
  const handleClose = () => {
    onClose();
  };

  const handleSubmit = async () => {
    await onSubmit();
  };

  return (
    <Modal show={show} onHide={handleClose}>
      <Modal.Header closeButton>
        <Modal.Title>Delete</Modal.Title>
      </Modal.Header>
      <Modal.Body>{message}</Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
        <Button variant="danger" onClick={handleSubmit}>
          Delete
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default DeleteModal;
