import React, { useState, useEffect } from "react";
import { Col, Row, Button } from "react-bootstrap";
import ListGroup from "react-bootstrap/ListGroup";
import { useDispatch } from "react-redux";
import { LinkContainer } from "react-router-bootstrap";

import Carousel from "./Carousel";
import Rating from "../common/Rating";
import { addItemToCart } from "../../features/cart/cartReducers";

const ProductPage = ({ product }) => {
  const [livePrice, setLivePrice] = useState(null);
  const { id, name, quantity, price, rate, description, images, num_comments } =
    product;
  const [status, product_price] =
    quantity === 0 ? ["Out of Stock", "Out of Stock"] : ["In Stock", price];
  const dispatch = useDispatch();

  const handleAddToCart = () => {
    dispatch(addItemToCart({ item: product }));
  };

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/product_update/");

    ws.onmessage = (event) => {
      const content = JSON.parse(event.data);

      if (content["product_id"] === id) {
        setLivePrice(content["new_price"]);
      }
    };

    return () => {
      ws.close();
    };
  }, [id]);

  return (
    <Row>
      <Col md={6}>
        <Carousel items={images} />
      </Col>

      <Col md={6}>
        <h2 className="bold line">{name}</h2>
        <Row>
          <Col md={8} className="info_box_container">
            <div className="line">
              <Rating value={rate} text={<> of {num_comments} reviews</>} />
            </div>
            <div className="line">
              <strong>Price: {livePrice ? livePrice : product_price}</strong>{" "}
            </div>
            <p>
              <strong>Description:</strong> {description}
            </p>
          </Col>

          <Col md={4} className="buy_box_container">
            <ListGroup className="text-center">
              <ListGroup.Item key="status">{status}</ListGroup.Item>
              {quantity > 0 && (
                <>
                  <ListGroup.Item key="add-to-cart">
                    <LinkContainer to={"/cart"}>
                      <Button
                        onClick={() => handleAddToCart()}
                        variant="primary"
                      >
                        Add to Cart
                      </Button>
                    </LinkContainer>
                  </ListGroup.Item>
                </>
              )}
            </ListGroup>
          </Col>
        </Row>
      </Col>
    </Row>
  );
};

export default ProductPage;
