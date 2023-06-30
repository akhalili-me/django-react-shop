import React, { useState } from "react";
import { useSelector} from "react-redux";
import { useEffect } from "react";
import { fetchUserAddresses } from "../utility/api/address";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import CartItems from "../components/cart/CartItems";
import AddressItem from "../components/checkout/AddressItem";

const Checkout = () => {
    const [addresses, setAddresses] = useState([]);
    const [selectedAddressId, setSelectedAddressId] = useState();
    const cart = useSelector((state) => state.cart);

    const onChangeAddress = (event) => {
        const selectedId = event.target.value
        setSelectedAddressId(selectedId);
    };
    
    useEffect(() => {
        const getUserAddresses = async () => {
            const { data } = await fetchUserAddresses();
            setAddresses(data);
        };
        getUserAddresses();
    }, []);

    const userAddresses = addresses.map((address) => (
        <AddressItem
            key={address.id}
            address={address}
            selectedAddressId={selectedAddressId}
            onChangeAddress={onChangeAddress}
        />
    ));
    
    const onPayClick = () => {
        //TODO
    }
    return (
        <>
            <h1 className="py-3">Choose your address</h1>
            <Form>{userAddresses}</Form>
            <h1 className="py-3">Order Products</h1>
            <CartItems items={cart.items} />
            <h3 className="py-3">
                <strong>Total:</strong>${cart.total}
            </h3>
            <Button onClick={onPayClick} className="pay_button" variant="success">Pay</Button>
        </>
    );
};

export default Checkout;
