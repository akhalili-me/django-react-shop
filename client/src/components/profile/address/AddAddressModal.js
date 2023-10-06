import React, { useState } from "react";
import { Modal, Form, Button, Col, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { addAddress } from "../../../features/address/addressOperations/addressOperationsReducers";

const AddAddressModal = ({ show, onClose }) => {
  const dispatch = useDispatch();

  const stateOptions = useSelector((state) => state.location.states);
  const [cityOptions, setCityOptions] = useState(null);
  const [isSelectCityDisabled, setIsSelectCityDisabled] = useState(true);

  const [formData, setFormData] = useState({
    state: "",
    city: "",
    phone: "",
    postal_code: "",
    street_address: "",
    house_number: "",
  });

  const handleSubmit = async (event) => {
    event.preventDefault();
    dispatch(
      addAddress({...formData})
    );
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
                onChange={(e) => {
                  const selectedState = e.target.value;
                  setFormData({...formData, state: selectedState});
                  setCityOptions(stateOptions.find((s) => s.name === selectedState)?.cities ?? null);
                  setIsSelectCityDisabled(selectedState === "Default");
                }}
                name="state"
              >
                <option value="Default">State</option>
                {stateOptions?.map((state) => (
                  <option key={state.id} value={state.name}>
                    {state.name}
                  </option>
                ))}
              </Form.Select>
              <Form.Control
                className="mt-3"
                name="phone"
                type="tel"
                onChange={(e) => setFormData({...formData, phone: e.target.value})}
                placeholder="Phone number"
                pattern="\d{11}"
                required
              />
            </Col>
            <Col md={6}>
              <Form.Select
                onChange={(e) => setFormData({...formData, city: e.target.value})}
                name="city"
                disabled={isSelectCityDisabled}
              >
                <option>City</option>
                {cityOptions?.map((city, index) => (
                  <option key={index} value={city}>
                    {city}
                  </option>
                ))}
              </Form.Select>
              <Form.Control
                className="mt-3"
                type="text"
                name="postal_code"
                onChange={(e) => setFormData({...formData, postal_code: e.target.value})}
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
                name="street_address"
                onChange={(e) => setFormData({...formData, street_address: e.target.value})}
                placeholder="Street address"
                required
              />
            </Col>
            <Col md={2}>
              <Form.Control
                className="mt-3"
                type="number"
                onChange={(e) => setFormData({...formData, house_number: e.target.value})}
                name="house_number"
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
