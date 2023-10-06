import React, { useEffect, useState } from "react";
import { Modal, Form, Button, Col, Row } from "react-bootstrap";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { useDispatch, useSelector } from "react-redux";
import { getAddressById } from "../../../features/address/addressDetails/addressDetailsReducers";
import { getUserAddresses } from "../../../features/address/addressList/addressListReducers";
import { updateAddress } from "../../../features/address/addressOperations/addressOperationsReducers";
import Loader from "../../common/Loader";
import Message from "../../common/Message";

const EditAddressModal = ({ show, onClose, addressId }) => {
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

  const { address, loading, error } = useSelector(
    (state) => state.addressDetails
  );

  useEffect(() => {
    dispatch(getAddressById(addressId));
  }, [addressId, dispatch]);

  useEffect(() => {
    if (address) {
      setFormData({
        state: address.state,
        city: address.city,
        phone: address.phone,
        postal_code: address.postal_code,
        street_address: address.street_address,
        house_number: address.house_number,
      });
      setCityOptions(
        stateOptions.find((s) => s.name === address.state)?.cities
      );
      setIsSelectCityDisabled(false);
    }
  }, [address]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    dispatch(
      updateAddress({
        id: addressId,
        ...formData,
      })
    );
    onClose();
  };

  return (
    <Modal show={show} onHide={onClose} dialogClassName="wider-modal-dialog">
      <Modal.Header closeButton>
        <Modal.Title>Edit Address</Modal.Title>
      </Modal.Header>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        <Form onSubmit={handleSubmit}>
          <Modal.Body>
            <Row>
              <Col md={6}>
                <Form.Select
                  aria-label="Default select example"
                  onChange={(e) => {
                    const selectedState = e.target.value;
                    setFormData({ ...formData, state: selectedState });
                    setCityOptions(
                      stateOptions.find((s) => s.name === selectedState)
                        ?.cities ?? null
                    );
                    setIsSelectCityDisabled(selectedState === "Default");
                  }}
                  name="state"
                  value={formData.state}
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
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                  value={formData.phone}
                  placeholder="Phone number"
                  pattern="\d{11}"
                  required
                />
              </Col>
              <Col md={6}>
                <Form.Select
                  onChange={(e) =>
                    setFormData({ ...formData, city: e.target.value })
                  }
                  aria-label="Default select example"
                  name="city"
                  value={formData.city}
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
                  value={formData.postal_code}
                  onChange={(e) =>
                    setFormData({ ...formData, postal_code: e.target.value })
                  }
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
                  value={formData.street_address}
                  onChange={(e) =>
                    setFormData({ ...formData, street_address: e.target.value })
                  }
                  placeholder="Street address"
                  required
                />
              </Col>
              <Col md={2}>
                <Form.Control
                  className="mt-3"
                  type="number"
                  onChange={(e) =>
                    setFormData({ ...formData, house_number: e.target.value })
                  }
                  value={formData.house_number}
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
      )}
    </Modal>
  );
};

export default EditAddressModal;
