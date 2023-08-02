import React from "react";
import { Button, Col, Row, ListGroup } from "react-bootstrap";
import { useSelector, useDispatch } from "react-redux";
import CartItems from "../components/cart/CartItems";
import { Link } from "react-router-dom";
import Message from "../components/common/Message";
import { clearAllItmesInCart } from "../features/cart/cartReducers";

const Cart = () => {
  const cart = useSelector((state) => state.cart);
  const dispatch = useDispatch();

  const handleClearCart = () => {
      dispatch(clearAllItmesInCart());
  };

  return (
    <>
      {cart.items?.length === 0 ? (
        <Message
          message={"Please Add a product to continiue."}
          variant={"info"}
        />
      ) : (
        <div>
          <h1 className="py-3">
            Shopping Cart{" "}
            <Button onClick={() => handleClearCart()} variant="danger">
              Clear Cart
            </Button>
          </h1>
          <Row>
            <Col md={9}>
              <CartItems items={cart.items} />
            </Col>
            <Col md={3}>
              <ListGroup className="checkout_sidebar">
                <ListGroup.Item>
                  <span className="bold">Items: </span> {cart.items.length}
                </ListGroup.Item>
                <ListGroup.Item>
                  <span className="bold">Total Price: </span> ${cart.total}
                </ListGroup.Item>
                <ListGroup.Item>
                  <Link to={"/checkout"}>
                    <Button variant="success">Checkout</Button>
                  </Link>
                </ListGroup.Item>
              </ListGroup>
            </Col>
          </Row>
        </div>
      )}
    </>
  );
};

export default Cart;
