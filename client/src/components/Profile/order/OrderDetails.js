import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import { getOrderById } from "../../../features/order/orderDetails/orderDetailsReducer";
import { useDispatch, useSelector } from "react-redux";
import OrderItems from "../../checkout/OrderItems";
import Loader from "../../common/Loader";
import Message from "../../common/Message";

const OrderDetails = () => {
  const { id } = useParams();
  const dispatch = useDispatch();

  const { order, loading, error } = useSelector((state) => state.orderDetails);

  useEffect(() => {
    dispatch(getOrderById({ orderId: id }));
  }, [dispatch, id]);

  return (
    <>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        <div>
          <h2 className="py-2">Order ID: {order?.id}</h2>
          <p>
            <strong>Address: </strong> {order?.full_address}
          </p>
          <p>
            <strong>Payment Status: </strong> {order.payment?.status}{" "}
            <strong>Payment Method: </strong> {order.payment?.payment_method}
          </p>
          <p>
            <strong>Total: </strong> ${order.total}{" "}
          </p>
          <OrderItems items={order?.order_items} />
        </div>
      )}
    </>
  );
};

export default OrderDetails;
