import React, { useEffect } from "react";
import { useParams } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import { Routes, Route } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import ProductPage from "../components/product/ProductPage";
import Features from "../components/product/Features";
import { useSelector, useDispatch } from "react-redux";
import { getProductDetails } from "../features/product/productDetails/productDetailsReducers";
import Comments from "../components/product/Comments";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";

const Product = () => {
  const dispatch = useDispatch();
  const { product, loading, error } = useSelector(
    (state) => state.productDetails
  );
  const { id } = useParams();

  useEffect(() => {
    dispatch(getProductDetails(id));
  }, [id, dispatch]);

  return (
    <>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        <div>
          {" "}
          <ProductPage product={product} />
          <Nav fill variant="tabs">
            <Nav.Item>
              <LinkContainer to={"reviews"}>
                <Nav.Link>Reviews</Nav.Link>
              </LinkContainer>
            </Nav.Item>
            <Nav.Item>
              <LinkContainer to={"features"}>
                <Nav.Link>Features</Nav.Link>
              </LinkContainer>
            </Nav.Item>
          </Nav>
        </div>
      )}

      <Routes>
        <Route path="/reviews" element={<Comments productId={id} />} />
        <Route path="/features" element={<Features productId={id} />} />
      </Routes>
    </>
  );
};

export default Product;
