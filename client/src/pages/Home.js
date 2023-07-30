import React, { useEffect, useMemo } from "react";
import Carousel from "../components/HomeSwiper";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import CategoryCard from "../components/category/CategoryCard";
import ProductCard from "../components/product/ProductCard";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import {
  getBestSellingProducts,
  getMostViewedProducts,
  getNewestProducts,
} from "../features/product/homeProductsList/homeProductsReducers";

const Home = () => {
  const dispatch = useDispatch();
  const parentCategories = useSelector((state) =>
    state.category.categories.filter((c) => c.parent === null)
  );
  const newestProducts = useSelector((state) => state.homeproducts.newest);
  const bestsellingProducts = useSelector((state) => state.homeproducts.newest);
  const mostViewedProducts = useSelector((state) => state.homeproducts.newest);

  useEffect(() => {
    dispatch(getNewestProducts());
    dispatch(getBestSellingProducts());
    dispatch(getMostViewedProducts());
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

      {newestProducts.loading ? (
        <Loader />
      ) : newestProducts.error ? (
        <Message variant={"danger"} message={newestProducts.error} />
      ) : (
        <>
          <Row xs={1} md={2} className="g-4">
            {newestProducts.products.map((product) => (
              <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                <ProductCard product={product} />
              </Col>
            ))}
          </Row>
        </>
      )}

      <h1 className="py-4">Bestselling Products</h1>

      {bestsellingProducts.loading ? (
        <Loader />
      ) : bestsellingProducts.error ? (
        <Message variant={"danger"} message={bestsellingProducts.error} />
      ) : (
        <>
          <Row xs={1} md={2} className="g-4">
            {bestsellingProducts.products.map((product) => (
              <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                <ProductCard product={product} />
              </Col>
            ))}
          </Row>
        </>
      )}
      <h1 className="py-4">Most Viewed Products</h1>

      {mostViewedProducts.loading ? (
        <Loader />
      ) : mostViewedProducts.error ? (
        <Message variant={"danger"} message={mostViewedProducts.error} />
      ) : (
        <>
          <Row xs={1} md={2} className="g-4">
            {mostViewedProducts.products.map((product) => (
              <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                <ProductCard product={product} />
              </Col>
            ))}
          </Row>
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
