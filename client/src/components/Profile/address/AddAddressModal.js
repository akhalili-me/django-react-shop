import React, { useCallback, useEffect, useState } from "react";
import { Modal, InputGroup, Form, Button, Col, Row } from "react-bootstrap";
import { addAddress } from "../../../utility/api/address";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { useDispatch, useSelector } from "react-redux";

const AddAddressModal = ({ show, onClose, addToAddressState }) => {
  const dispatch = useDispatch();
  const states = useSelector((state) => state.location.states);

  const [address, setAddress] = useState({});
  const [selectCityDisabled, setSelectCityDisabled] = useState(true);
  const [cities, setCities] = useState(null);

  const handleFieldChange = useCallback(
    (event) => {
      const { name, value } = event.target;
      setAddress({
        ...address,
        [name]: value,
      });

      if (name === "state") {
        if (value === "default") {
          setCities(null);
          setSelectCityDisabled(true);
        } else {
          setCities(states.find((c) => c.name === value).cities);
          setSelectCityDisabled(false);
        }
      }
    },
    [address, states]
  );

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await addAddress(address);
      addToAddressState(address)
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
                <option value="default">State</option>
                {states?.map((state) => (
                  <option key={state.id} value={state.name}>
                    {state.name}
                  </option>
                ))}
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
                name="city"
                disabled={selectCityDisabled}
              >
                <option>City</option>
                {cities?.map((city, index) => (
                  <option key={index} value={city}>
                    {city}
                  </option>
                ))}
              </Form.Select>
              <Form.Control
                className="mt-3"
                type="text"
                name="postal_code"
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
                name="street_address"
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
