import React, { useEffect } from "react";
import { getProductsByNameSearch } from "../features/product/productList/productListReducers";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import Message from "../components/common/Message";
import Loader from "../components/common/Loader";
import { Col, Row } from "react-bootstrap";
import ProductCard from "../components/product/ProductCard";
import Pagination from "../components/common/Pagination";

const ProductSearch = () => {
  const dispatch = useDispatch();
  const { q } = useParams();
  const { products, loading, error, count } = useSelector(
    (state) => state.productList
  );

  useEffect(() => {
    console.log(q);
    dispatch(getProductsByNameSearch({ q }));
  }, [dispatch, q]);

  return (
    <>
      <h2 className="py-4">You searched for: {q}</h2>
      <Row xs={1} md={2} className="g-4">
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant={"danger"} message={error} />
        ) : products.length === 0 ? (
          <h3>No product available!</h3>
        ) : (
          products.map((product) => (
            <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
              <ProductCard product={product} />
            </Col>
          ))
        )}
      </Row>
      <Pagination count={count} paginateBy={2} />
    </>
  );
};

export default ProductSearch;
