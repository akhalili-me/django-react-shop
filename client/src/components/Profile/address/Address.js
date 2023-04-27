import React, { useEffect, useState } from "react";
import { ListGroup, Button, Row, Col, ButtonGroup } from "react-bootstrap";
import AddAddressModal from "./AddAddressModal";
import EditAddressModal from "./EditAddressModal";
import { fetchUserAddresses } from "../../../utility/api/address";

const Address = () => {
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [addresses, setAddresses] = useState([]);
  const [addressId, setAddressId] = useState(0);

  const handleShowAddModal = () => {
    setShowAddModal(true);
  };

  const handleShowEditModal = async (event) => {
    const { dataset } = event.target;
    const id = parseInt(dataset.addressid);
    setAddressId(id)
    setShowEditModal(true);
  };

  const handleCloseModal = () => {
    setShowAddModal(false);
    setShowEditModal(false);
  };

  useEffect(() => {
    const getAddresses = async () => {
      const { data } = await fetchUserAddresses();
      setAddresses(data);
    };

    getAddresses();
  }, []);


  const updateAddressState = (address) => {
    const updatedAddressIndex = addresses.findIndex((a) => a.id === address.id);
    addresses[updatedAddressIndex] = address;
    setAddresses(addresses);
  };

  return (
    <>
      <AddAddressModal show={showAddModal} onClose={handleCloseModal} />
      <EditAddressModal
        show={showEditModal}
        onClose={handleCloseModal}
        addressId={addressId}
        updateAddressState={updateAddressState}
      />

      <Button className="mb-3" onClick={handleShowAddModal}>
        Add new Address
      </Button>
      <ListGroup>
        {addresses.map((address) => (
          <ListGroup.Item key={address.id}>
            <Row>
              <Col md={10}>
                <p>{address.street_address}</p>
                <p>
                  <strong>State: </strong>
                  {address.state} <strong>City: </strong>
                  {address.city}
                </p>
                <p>
                  <strong>Phone: </strong>
                  {address.phone}
                </p>
                <p>
                  <strong>Pelak: </strong>
                  {address.house_number}
                </p>
                <p>
                  <strong>Postal Code: </strong>
                  {address.postal_code}
                </p>
              </Col>
              <Col md={2}>
                <ButtonGroup className="comment_buttons">
                  <Button
                    name="edit"
                    variant="warning"
                    onClick={handleShowEditModal}
                    data-addressid={address.id}
                  >
                    <i
                      class="fas fa-edit"
                      style={{ pointerEvents: "none" }}
                    ></i>
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
        ))}
      </ListGroup>
    </>
  );
};

export default Address;
