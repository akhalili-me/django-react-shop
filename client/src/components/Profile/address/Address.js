import React, { useEffect, useState } from "react";
import { ListGroup, Button, Row, Col, ButtonGroup } from "react-bootstrap";
import AddAddressModal from "./AddAddressModal";
import EditAddressModal from "./EditAddressModal";
import { fetchUserAddresses,deleteAddress } from "../../../utility/api/address";
import DeleteModal from "../../common/DeleteModal";
import { setAlarm } from "../../../features/alert/alarmSlice";
import { useDispatch } from "react-redux";

const Address = () => {
  const dispatch = useDispatch();
  const [showAddModal, setShowAddModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false );
  const [addresses, setAddresses] = useState([]);
  const [addressId, setAddressId] = useState(0);

  const handleShowAddModal = () => {
    setShowAddModal(true);
  };
  
  const handleShowModal = async (event) => {
    const { name, dataset } = event.target;
    const id = parseInt(dataset.addressid);
    

    if (name === "delete") {
      setShowDeleteModal(true);
    } else if (name === "edit") {
      setShowEditModal(true);
    }

    setAddressId(id)
    console.log(id);
  };

  const handleCloseModal = () => {
    setShowAddModal(false);
    setShowEditModal(false);
    setShowDeleteModal(false)
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

  const addToAddressState = (address) => {
    setAddresses([...addresses, address]);
  }

  const removeAddress = async () => {
    try {
      await deleteAddress(addressId);
      const updatedAddresses = addresses.filter(
        (address) => address.id !== addressId
      );
      setAddresses(updatedAddresses);
      dispatch(
        setAlarm({
          message: "Address deleted successfully",
          type: "success",
          show: true,
        })
      );
    } catch (error) {
      dispatch(
        setAlarm({
          message: error.message,
          type: "danger",
          show: true,
        })
      );
    } finally {
      setShowDeleteModal(false);
    }
  };
  return (
    <>
      <AddAddressModal
        show={showAddModal}
        onClose={handleCloseModal}
        addToAddressState={addToAddressState}
      />
      <EditAddressModal
        show={showEditModal}
        onClose={handleCloseModal}
        addressId={addressId}
        updateAddressState={updateAddressState}
      />
      <DeleteModal
        show={showDeleteModal}
        onSubmit={removeAddress}
        onClose={handleCloseModal}
        message={"Are you sure to delete this address?"}
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
                    onClick={handleShowModal}
                    data-addressid={address.id}
                  >
                    <i
                      class="fas fa-edit"
                      style={{ pointerEvents: "none" }}
                    ></i>
                  </Button>
                  <Button
                    name="delete"
                    variant="danger"
                    onClick={handleShowModal}
                    data-addressid={address.id}
                  >
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
