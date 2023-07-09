import React, {useState } from "react";
import { Modal, Form, Button, Col, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { addAddress } from "../../../features/address/addressOperations/addressOperationsReducers";
import { setAlarm } from "../../../features/alert/alarmSlice";
import Loader from "../../common/Loader";

const AddAddressModal = ({ show, onClose }) => {
	const dispatch = useDispatch();
	const statesOptions = useSelector((state) => state.location.states);
	const [cityOptions, setCityOptions] = useState(null);
	const [isSelectCityDisabled, setIsSelectCityDisabled] = useState(true);

	const [state, setState] = useState("");
	const [city, setCity] = useState("");
	const [phone, setPhone] = useState("");
	const [postalCode, setPostalCode] = useState("");
	const [streetAddress, setStreetAddress] = useState("");
	const [houseNumber, setHouseNumber] = useState("");

	const { loading, error, success } = useSelector(
		(state) => state.addressOperations
	);

	const handleSubmit = async (event) => {
		event.preventDefault();
		dispatch(
			addAddress({
				state: state,
				city: city,
				phone: phone,
				postal_code: postalCode,
				street_address: streetAddress,
				house_number: houseNumber,
			})
		);

		if (success) {
			dispatch(
				setAlarm({
					message: "Address added successfuly.",
					type: "success",
				})
			);
		} else if (success === false) {
			dispatch(setAlarm({ message: error, type: "danger" }));
		}

		onClose();
	};

	return (
		<Modal
			show={show}
			onHide={onClose}
			dialogClassName="wider-modal-dialog"
		>
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
									if (e.target.value === "Default") {
										setCityOptions(null);
										setIsSelectCityDisabled(true);
									} else {
										setState(e.target.value);
										setCityOptions(
											statesOptions.find(
												(c) => c.name === e.target.value
											).cities
										);
										setIsSelectCityDisabled(false);
									}
								}}
								name="state"
							>
								<option value="default">State</option>
								{statesOptions?.map((state) => (
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
								placeholder="Phone number"
								pattern="\d{11}"
								required
							/>
						</Col>
						<Col md={6}>
							<Form.Select
								onChange={(e) => setCity(e.target.value)}
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
								onChange={(e) =>
									setStreetAddress(e.target.value)
								}
								placeholder="Street address"
								required
							/>
						</Col>
						<Col md={2}>
							<Form.Control
								className="mt-3"
								type="number"
								onChange={(e) => setHouseNumber(e.target.value)}
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
						{loading ? <Loader /> : "Submit"}
					</Button>
				</Modal.Footer>
			</Form>
		</Modal>
	);
};

export default AddAddressModal;
