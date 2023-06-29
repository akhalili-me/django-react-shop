import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useEffect } from "react";
import { fetchUserAddresses } from "../utility/api/address";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import CartItems from "../components/cart/CartItems";

const Checkout = () => {
    const [addresses, setAddresses] = useState([]);
    const [selectedAddressId, setSelectedAddressId] = useState();
    const cart = useSelector((state) => state.cart);

    const onChangeAddress = (event) => {
        setSelectedAddressId(event.target.value);
    };

    useEffect(() => {
        const getUserAddresses = async () => {
            const { data } = await fetchUserAddresses();
            setAddresses(data);
        };
        getUserAddresses();
    }, []);

    const userAddresses = addresses.map((address) => {
        const fullAddress = `${address.state}, ${address.city} ${address.street_address} ${address.house_number} ${address.postal_code}`;

        return (
            <Form.Check
                name="address"
                checked={selectedAddressId === address.id}
                type="radio"
                value={address.id}
                label={fullAddress}
                onChange={onChangeAddress}
            />
        );
    });

    return (
        <>
            <h1>Choose your address</h1>
            <Form>{userAddresses}</Form>
            <h1>Order Products</h1>
            <CartItems items={cart.items} />
            <h1>Checkout</h1>
            <h3>
                <strong>Total:</strong> {cart.total}
            </h3>
            <Button variant="success">Pay</Button>
        </>
    );
};

export default Checkout;
