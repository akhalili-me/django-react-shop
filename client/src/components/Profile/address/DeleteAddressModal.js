import React from "react";
import { Modal, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { setAlarm } from "../../../features/alert/alarmSlice";
import Loader from "../../common/Loader";
import { deleteAddress } from "../../../features/address/addressOperations/addressOperationsReducers";

const DeleteAddressModal = ({ show, addressId, onClose }) => {
    const dispatch = useDispatch();
    const handleSubmit = async (event) => {
        event.preventDefault();
        dispatch(deleteAddress(addressId));
        onClose();
    };

    return (
        <Modal show={show} onHide={onClose}>
            <Modal.Header closeButton>
                <Modal.Title>Delete</Modal.Title>
            </Modal.Header>
            <Modal.Body>Are you sure to delete this Address?</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={onClose}>
                    Close
                </Button>
                <Button variant="danger" onClick={handleSubmit}>
                    Delete
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default DeleteAddressModal;
