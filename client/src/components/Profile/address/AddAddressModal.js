import React, { useEffect, useState } from "react";
import { Modal, InputGroup, Form, Button, Col, Row } from "react-bootstrap";
import { addAddress } from "../../../utility/api/address";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { useDispatch } from "react-redux";

const AddAddressModal = ({ show, onClose, onSubmit }) => {
  const [address, setAddress] = useState({});
  const dispatch = useDispatch();

  const handleFieldChange = (event) => {
    setAddress({
      ...address,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await addAddress(address);
      dispatch(
        setAlarm({
          message: "Address added successfully.",
          type: "success",
          show: true,
        })
      );
    } catch (error) {
      dispatch(
        setAlarm({
          message: "Failed to add address, try again.",
          type: "danger",
          show: true,
        })
      );
    }

    onClose();
  };

  return (
    <Modal show={show} onHide={onClose} dialogClassName="wider-modal-dialog">
      <Modal.Header closeButton>
        <Modal.Title>Add Address</Modal.Title>
      </Modal.Header>
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          <Row>
            <Col md={6}>
              <Form.Select
                aria-label="Default select example"
                onChange={handleFieldChange}
                name="state"
              >
                <option>State</option>
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </Form.Select>
              <Form.Control
                className="mt-3"
                name="phone"
                type="tel"
                onChange={handleFieldChange}
                placeholder="Phone number"
                pattern="\d{11}"
                required
              />
            </Col>
            <Col md={6}>
              <Form.Select
                onChange={handleFieldChange}
                aria-label="Default select example"
                name="city"
              >
                <option>City</option>
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </Form.Select>
              <Form.Control
                className="mt-3"
                type="text"
                name="postalCode"
                onChange={handleFieldChange}
                placeholder="Postal code"
                pattern="\d{10}"
                required
              />
            </Col>
          </Row>
          <Row>
            <Col md={10}>
              <Form.Control
                className="mt-3"
                type="text"
                name="streetAddress"
                onChange={handleFieldChange}
                placeholder="Street address"
                required
              />
            </Col>
            <Col md={2}>
              <Form.Control
                className="mt-3"
                type="number"
                onChange={handleFieldChange}
                name="houseNumber"
                placeholder="Pelak"
                required
              />
            </Col>
          </Row>
        </Modal.Body>

        <Modal.Footer>
          <Button onClick={onClose} variant="secondary">
            Close
          </Button>
          <Button type="submit" variant="primary">
            Submit
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default AddAddressModal;
