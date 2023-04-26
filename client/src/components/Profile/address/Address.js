import React, { useState } from "react";
import { ListGroup, Button, Row, Col, ButtonGroup } from "react-bootstrap";
import AddAddressModal from "./AddAddressModal";
const Address = () => {
  const [showAddModal,setShowAddModal] = useState(false)

  const handleShowAddModal = () => {
    setShowAddModal(true)
  }

  const handleCloseModal = () => {
    setShowAddModal(false)
  }

  return (
    <>
      <AddAddressModal
      show={showAddModal}
      onClose={handleCloseModal}
      />
      <Button className="mb-3" onClick={handleShowAddModal}>Add new Address</Button>
      <ListGroup>
        <ListGroup.Item>
          <Row>
            <Col md={10}></Col>
            <Col md={2}>
              <ButtonGroup className="comment_buttons">
                <Button name="edit" variant="warning">
                  <i class="fas fa-edit" style={{ pointerEvents: "none" }}></i>
                </Button>
                <Button name="delete" variant="danger">
                  <i
                    className="fas fa-trash"
                    style={{ pointerEvents: "none" }}
                  ></i>
                </Button>
              </ButtonGroup>
            </Col>
          </Row>
        </ListGroup.Item>
      </ListGroup>
    </>
  );
};

export default Address;
