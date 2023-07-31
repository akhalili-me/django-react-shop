import React, { useEffect, useMemo } from "react";
import Carousel from "../components/HomeSwiper";
import { Col, Row, Tab, Tabs } from "react-bootstrap";
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
  const { newest, bestselling, mostViewed } = useSelector(
    (state) => state.homeProducts
  );

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
      <h1 className="py-4">Products</h1>

      <Tabs
        defaultActiveKey="Newest"
        className="mb-3"
        fill
      >
        <Tab eventKey="Newest" title="Newest">
          {newest.loading ? (
            <Loader />
          ) : newest.error ? (
            <Message variant={"danger"} message={newest.error} />
          ) : (
            <>
              <Row xs={1} md={2} className="g-4">
                {newest.products?.map((product) => (
                  <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                    <ProductCard product={product} />
                  </Col>
                ))}
              </Row>
            </>
          )}
        </Tab>
        <Tab eventKey="Bestselling" title="Bestselling">
          {bestselling.loading ? (
            <Loader />
          ) : bestselling.error ? (
            <Message variant={"danger"} message={bestselling.error} />
          ) : (
            <>
              <Row xs={1} md={2} className="g-4">
                {bestselling.products?.map((product) => (
                  <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                    <ProductCard product={product} />
                  </Col>
                ))}
              </Row>
            </>
          )}
        </Tab>
        <Tab eventKey="Most Viewed" title="Most Viewed">
          {mostViewed.loading ? (
            <Loader />
          ) : mostViewed.error ? (
            <Message variant={"danger"} message={mostViewed.error} />
          ) : (
            <>
              <Row xs={1} md={2} className="g-4">
                {mostViewed.products?.map((product) => (
                  <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                    <ProductCard product={product} />
                  </Col>
                ))}
              </Row>
            </>
          )}
        </Tab>
      </Tabs>

      <h1 className="py-4">Categories</h1>
      <Row xs={1} md={2} className="">
        {categoryCards}
      </Row>
    </div>
  );
};

export default Home;
