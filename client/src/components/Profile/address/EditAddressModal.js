import React, { useCallback, useEffect, useState } from "react";
import { Modal, InputGroup, Form, Button, Col, Row } from "react-bootstrap";
import { fetchAddressById, updateAddress } from "../../../utility/api/address";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { useDispatch, useSelector } from "react-redux";

const EditAddressModal = ({ show, onClose, updateAddressState, addressId }) => {
  const [address, setAddress] = useState({});
  const dispatch = useDispatch();
  const states = useSelector((state) => state.location.states);
  const [selectCityDisabled, setSelectCityDisabled] = useState(true);
  const [cities, setCities] = useState(null);

  useEffect(() => {
    const getAddressAndSetCities = async () => {
      const { data } = await fetchAddressById(addressId);
      setAddress(data);
      setCities(states.find((c) => c.name === data?.state)?.cities);
      setSelectCityDisabled(false);
    };

    if (addressId !== 0) {
      getAddressAndSetCities();
    } else {
      setCities(null);
      setSelectCityDisabled(true);
    }
  }, [addressId, states]);

  const handleFieldChange = useCallback(
    (event) => {
      const { name, value } = event.target;
      setAddress({
        ...address,
        [name]: value,
      });

      if (name === "state") {
        if (value === "default") {
          setSelectCityDisabled(true);
          setCities(null);
        } else {
          setCities(states.find((c) => c.name === value)?.cities);
          setSelectCityDisabled(false);
        }
      }
    },
    [address, states]
  );

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await updateAddress(address);
      updateAddressState(address)
      dispatch(
        setAlarm({
          message: "Address updated successfully.",
          type: "success",
          show: true,
        })
      );
    } catch (error) {
      dispatch(
        setAlarm({
          message: "Failed to update address, try again.",
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
        <Modal.Title>Edit Address</Modal.Title>
      </Modal.Header>
      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          <Row>
            <Col md={6}>
              <Form.Select
                aria-label="Default select example"
                onChange={handleFieldChange}
                name="state"
                value={address?.state || "default"}
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
                value={address.phone || ""}
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
                value={address?.city || "default"}
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
                value={address.postal_code || ""}
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
                value={address.street_address || ""}
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
                value={address.house_number || ""}
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
            Update
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default EditAddressModal;
