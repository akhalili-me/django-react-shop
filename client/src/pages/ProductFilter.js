import React, { useEffect, useState, useMemo } from "react";
import { Col, Row } from "react-bootstrap";
import Filter from "../components/Filter";
import { useParams } from "react-router-dom";
import { useSearchParams } from "react-router-dom";
import ProductCard from "../components/product/ProductCard";
import Pagination from "../components/common/Pagination";
import { getProductsByFilter } from "../features/product/productList/productListReducers";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";

const ProductFilter = () => {
  const dispatch = useDispatch();
  const [queryParams] = useSearchParams();
  const { id } = useParams();
  const { products, loading, error, count } = useSelector(
    (state) => state.productList
  );

  useEffect(() => {
    let params = "";

    const page = queryParams.get("page") || 1;
    // filters
    const min = queryParams.get("min") || 0;
    const max = queryParams.get("max") || 0;
    const sort = queryParams.get("sort") || "default";
    const has_selling_stock = queryParams.get("has_selling_stock") || false;

    if (page > 1) {
      params += `page=${page}&`;
    }

    if (min > 0) {
      params += `min=${min}&`;
    }

    if (max > 0) {
      params += `max=${max}&`;
    }

    if (sort !== "default") {
      params += `sort=${sort}&`;
    }

    if (has_selling_stock !== false) {
      params += `has_selling_stock=${has_selling_stock}&`;
    }
    dispatch(getProductsByFilter({ childCategoryId: id, params: params }));
  }, [id, queryParams, dispatch]);

  return (
    <>
      <div>
        <Row>
          <Col md={9}>
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
          </Col>
          <Col md={3}>
            <Filter />
          </Col>
        </Row>

        <Pagination count={count} paginateBy={2} />
      </div>
    </>
  );
};

export default ProductFilter;
