import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getUserOrders } from "../../../features/order/orderList/orderListReducers";
import { Button, ListGroup, Col, Row } from "react-bootstrap";
import Loader from "../../common/Loader";
import Message from "../../common/Message";
import { Link } from "react-router-dom";

const Orders = () => {
  const dispatch = useDispatch();
  const { orders, loading, error } = useSelector((state) => state.orderList);

  useEffect(() => {
    dispatch(getUserOrders());
  }, [dispatch]);

  return (
    <>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        <ListGroup>
          {orders.map((order) => (
            <ListGroup.Item>
              <Row>
                <Col md={10}>
                  <h2>Order ID: #{order.id}</h2>
                  <p>Status: {order.status}</p>
                  <p>Total: ${order.total}</p>
                  <p>Date: {order.created_at}</p>
                </Col>
                <Col md={2}>
                  <Link to={`/orders/${order.id}`}>
                    <Button variant="info">More info</Button>
                  </Link>
                </Col>
              </Row>
            </ListGroup.Item>
          ))}
        </ListGroup>
      )}
    </>
  );
};

export default Orders;
