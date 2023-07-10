import React, { useState } from "react";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import AddressItem from "../components/checkout/AddressItem";
import {addOrder} from "../utility/api/order";
import OrderItems from "../components/checkout/OrderItems";
import { useDispatch } from "react-redux";
import { getUserAddresses } from "../features/address/addressList/addressListReducers";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";


const Checkout = () => {
    const [selectedAddressId, setSelectedAddressId] = useState();
    const [shippingPrice] = useState(10);
    const cart = useSelector((state) => state.cart);

    const dispatch = useDispatch()

    useEffect(() => {
        dispatch(getUserAddresses())
    }, [dispatch]);

    const {addresses,loading,error} = useSelector(state => state.addressList)

    const userAddresses = addresses.map((address) => (
        <AddressItem
            key={address.id}
            address={address}
            selectedAddressId={selectedAddressId}
            onChangeAddress={() => {
                setSelectedAddressId(address.id)
            }}
        />
    ));

    const onPayClick = async () => {
        const order_items = cart.items.map(item => ({
            product: item.product.id,
            quantity: item.quantity
        }));
        await addOrder(
            selectedAddressId,
            cart.total + shippingPrice,
            shippingPrice,
            order_items
        );
    };
    

    return (
        <>
            <h1 className="py-3">Choose your address</h1>
            <Form>
                {loading ? (
                    <Loader />
                ) : error ? (
                    <Message variant={"danger"} message={error} />
                ) : (
                    userAddresses
                )}
            </Form>
            <h1 className="py-3">Order Products</h1>
            <OrderItems items={cart.items} />
            <h3 className="py-3">
                <strong>Total:</strong>${cart.total}
            </h3>
            <Button
                onClick={onPayClick}
                className="pay_button"
                variant="success"
            >
                Pay
            </Button>
        </>
    );
};

export default Checkout;
