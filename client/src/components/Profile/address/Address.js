import React, { useEffect, useState } from "react";
import { ListGroup, Button, Row, Col, ButtonGroup } from "react-bootstrap";
import AddAddressModal from "./AddAddressModal";
import EditAddressModal from "./EditAddressModal";
import { useDispatch, useSelector } from "react-redux";
import { getUserAddresses } from "../../../features/address/addressList/addressListReducers";
import Loader from "../../common/Loader";
import Message from "../../common/Message";
import DeleteAddressModal from "./DeleteAddressModal";

const Address = () => {
  const dispatch = useDispatch();
  const [showAddModal, setShowAddModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [addressId, setAddressId] = useState(0);

  const { addresses, loading, error } = useSelector(
    (state) => state.addressList
  );

  useEffect(() => {
    dispatch(getUserAddresses());
  }, [dispatch]);

  return (
    <>
      <AddAddressModal show={showAddModal} onClose={() => setShowAddModal(false)} />
      <EditAddressModal
        show={showEditModal}
        onClose={() => setShowEditModal(false)}
        addressId={addressId}
      />
      <DeleteAddressModal
        show={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        addressId={addressId}
      />

      <Button className="mb-3" onClick={() => setShowAddModal(true)}>
        Add new Address
      </Button>

      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
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
                      onClick={() => {
                        setAddressId(address.id);
                        setShowEditModal(true);
                      }}
                    >
                      <i
                        class="fas fa-edit"
                        style={{
                          pointerEvents: "none",
                        }}
                      ></i>
                    </Button>
                    <Button
                      name="delete"
                      variant="danger"
                      onClick={() => {
                        setAddressId(address.id);
                        setShowDeleteModal(true);
                      }}
                    >
                      <i
                        className="fas fa-trash"
                        style={{
                          pointerEvents: "none",
                        }}
                      ></i>
                    </Button>
                  </ButtonGroup>
                </Col>
              </Row>
            </ListGroup.Item>
          ))}
        </ListGroup>
      )}
    </>
  );
};

export default Address;
