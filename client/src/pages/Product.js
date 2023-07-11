import React, {useEffect } from "react";
import { useParams } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import { Routes, Route } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import ProductPage from "../components/product/ProductPage";
import Features from "../components/product/Features";
import { useSelector,useDispatch } from "react-redux";
import { getProductDetails } from "../features/product/productDetails/productDetailsReducers";
import Comments from "../components/product/Comments"

const Product = () => {
  const dispatch = useDispatch()
  const product = useSelector(state => state.productDetails.product)
  const { id } = useParams();
  
  useEffect(() => {
    dispatch(getProductDetails(id))
  }, [id,dispatch]);

  return (
    <>
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

      <Routes>
        <Route path="/reviews" element={<Comments productId={id} />} />
        <Route path="/features" element={<Features productId={id} />} />
      </Routes>
      
    </>
  );
};

export default Product;
