import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import Nav from "react-bootstrap/Nav";
import { Routes, Route } from "react-router-dom";
import { LinkContainer } from "react-router-bootstrap";
import ProductPage from "../components/product/ProductPage";
import Reviews from "../components/product/Reviews";
import Features from "../components/product/Features";

const Product = () => {
  const [product, setProduct] = useState([]);
  const { id } = useParams();

  useEffect(() => {
    async function getProducts() {
      const response = await axios.get(`/products/${id}/`);
      const { data: product } = response;
      setProduct(product);
    }

    getProducts();
  }, [id]);

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
        <Route path="/reviews" element={<Reviews productId={id} />} />
        <Route path="/features" element={<Features productId={id} />} />
      </Routes>
      
    </>
  );
};

export default Product;
