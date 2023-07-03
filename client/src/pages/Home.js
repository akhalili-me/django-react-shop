import React, { useEffect, useState, useMemo } from "react";
import Carousel from "../components/HomeSwiper";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import CategoryCard from "../components/category/CategoryCard";
import ProductCard from "../components/product/ProductCard";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { getLatestProducts } from "../features/product/productReducers";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";

const Home = () => {
  const dispatch = useDispatch();
  const parentCategories = useSelector((state) =>
    state.category.categories.filter((c) => c.parent === null)
  );
  const { products, loading, error, count } = useSelector(
    (state) => state.product
  );

  useEffect(() => {
    dispatch(getLatestProducts());
  }, [dispatch]);

  const categoryCards = useMemo(() => {
    return parentCategories.map((category) => (
      <Col key={category.id} sm={4} md={4} lg={2} xl={2}>
        <Link to={`/category/${category.id}`}>
          <CategoryCard category={category} />
        </Link>
      </Col>
    ));
  }, [parentCategories]);

  return (
    <div>
      <Carousel />
      <h1 className="py-4">Latest Products</h1>

      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        <>
          <Row xs={1} md={2} className="g-4">
            {products.map((product) => (
              <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                <ProductCard product={product} />
              </Col>
            ))}
          </Row>
          <a className="">See More...</a>
        </>
      )}

      <h1 className="py-4">Categories</h1>
      <Row xs={1} md={2} className="">
        {categoryCards}
      </Row>
    </div>
  );
};

export default Home;
