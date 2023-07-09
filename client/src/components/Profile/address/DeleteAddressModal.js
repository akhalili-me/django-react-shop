import React from "react";
import { Modal, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { setAlarm } from "../../../features/alert/alarmSlice";
import Loader from "../../common/Loader";
import { deleteAddress } from "../../../features/address/addressOperations/addressOperationsReducers";
import { getUserAddresses } from "../../../features/address/addressList/addressListReducers";

const DeleteAddressModal = ({ show, addressId, onClose }) => {
    const dispatch = useDispatch();

    const {loading,error,success} = useSelector(state => state.addressOperations)

    const handleSubmit = async (event) => {
        event.preventDefault();
        dispatch(deleteAddress(addressId));

        if (success) {
            dispatch(getUserAddresses())
            dispatch(setAlarm({
                message: "Address successfully deleted.",
                type: "success"
            }))
        }else if (success === false)
        {
            dispatch(setAlarm({ message: error, type: "danger" }));
        }

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
                    {loading ? <Loader/> : "Delete"}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default DeleteAddressModal;
