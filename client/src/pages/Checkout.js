import React, { useState } from "react";
import { useSelector } from "react-redux";
import { useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import AddressItem from "../components/checkout/AddressItem";
import OrderItems from "../components/checkout/OrderItems";
import { useDispatch } from "react-redux";
import { getUserAddresses } from "../features/address/addressList/addressListReducers";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import { addOrder } from "../features/order/orderOperations/orderOperationsReducers";
import { useNavigate } from "react-router-dom";

const Checkout = () => {
  const [selectedAddressId, setSelectedAddressId] = useState();
  const [shippingPrice] = useState(10);
  const navigate = useNavigate();
  const cart = useSelector((state) => state.cart);

  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getUserAddresses());
  }, [dispatch]);

  const { addresses, loading, error } = useSelector(
    (state) => state.addressList
  );

  const { success } = useSelector((state) => state.orderOperations);

  const userAddresses = addresses.map((address) => (
    <AddressItem
      key={address.id}
      address={address}
      selectedAddressId={selectedAddressId}
      onChangeAddress={() => {
        setSelectedAddressId(address.id);
      }}
    />
  ));

  const onPayClick = async () => {
    const orderItems = cart.items.map((item) => ({
      product: item.product.id,
      quantity: item.quantity,
    }));

    dispatch(
      addOrder({
        addressId: selectedAddressId,
        totalPrice: cart.total + shippingPrice,
        paymentMethod: "saderat",
        shippingPrice,
        orderItems,
        navigator: navigate
      })
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
        <strong>Shipping Price:</strong>${shippingPrice}
      </h3>
      <h3 className="py-3">
        <strong>Total:</strong>${cart.total + shippingPrice}
      </h3>
      <Button onClick={onPayClick} className="pay_button" variant="success">
        Pay
      </Button>
    </>
  );
};

export default Checkout;
