import React, { useEffect, useState } from "react";
import { Modal, Form, Button, Col, Row } from "react-bootstrap";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { useDispatch, useSelector } from "react-redux";
import {getAddressById} from "../../../features/address/addressDetails/addressDetailsReducers"
import { getUserAddresses } from "../../../features/address/addressList/addressListReducers";
import { updateAddress } from "../../../features/address/addressOperations/addressOperationsReducers";

const EditAddressModal = ({ show, onClose, addressId }) => {
  const dispatch = useDispatch();
  const stateOptions = useSelector((state) => state.location.states);
  const [cityOptions, setCityOptions] = useState(null);
  const [isSelectCityDisabled, setIsSelectCityDisabled] = useState(true);

  const [state, setState] = useState("");
	const [city, setCity] = useState("");
	const [phone, setPhone] = useState("");
	const [postalCode, setPostalCode] = useState("");
	const [streetAddress, setStreetAddress] = useState("");
	const [houseNumber, setHouseNumber] = useState("");

  const {address,loading,error} = useSelector(state => state.addressDetails)
  const updateOperation = useSelector(state => state.adressOperations)

  useEffect(() => {
    if (show) {
      dispatch(getAddressById(addressId))


      if (error === null && loading === false) {
        setState(address.state)
        setCity(address.city)
        setPhone(address.phone)
        setPostalCode(address.postal_code)
        setStreetAddress(address.street_address)
        setHouseNumber(address.house_number)
  
        setCityOptions(stateOptions.find((s) => s.name === address.state)?.cities)
        setIsSelectCityDisabled(false)
      }

    }
  }, [dispatch, addressId]);

	const handleSubmit = async (event) => {
		event.preventDefault();
		dispatch(
			updateAddress({
        id: addressId,
				state: state,
				city: city,
				phone: phone,
				postal_code: postalCode,
				street_address: streetAddress,
				house_number: houseNumber,
			})
		);

		if (updateOperation.success) {
      dispatch(getUserAddresses())
			dispatch(
				setAlarm({
					message: "Address updated successfuly.",
					type: "success",
				})
			);
		} else if (updateOperation.success === false) {
			dispatch(setAlarm({ message: updateOperation.error, type: "danger" }));
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
                onChange={(e) => {
                  const selectedState = e.target.value;
                  setState(selectedState);
                  setCityOptions(stateOptions.find((s) => s.name === selectedState)?.cities ?? null);
                  setIsSelectCityDisabled(selectedState === "Default");
								}}
                name="state"
                value={state || "Default"}
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
                onChange={(e) => setPhone(e.target.value)}
                value={phone || ""}
                placeholder="Phone number"
                pattern="\d{11}"
                required
              />
            </Col>
            <Col md={6}>
              <Form.Select
                onChange={(e) => setCity(e.target.value)}
                aria-label="Default select example"
                name="city"
                value={city || "default"}
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
                value={postalCode || ""}
                onChange={(e) => setPostalCode(e.target.value)}
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
                value={streetAddress || ""}
                onChange={(e) => setStreetAddress(e.target.value)}
                placeholder="Street address"
                required
              />
            </Col>
            <Col md={2}>
              <Form.Control
                className="mt-3"
                type="number"
                onChange={(e) => setHouseNumber(e.target.value)}
                value={houseNumber || ""}
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
