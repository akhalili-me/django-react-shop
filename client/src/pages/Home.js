import React, { useEffect, useState, useMemo } from "react";
import Carousel from "../components/HomeSwiper";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import CategoryCard from "../components/category/CategoryCard";
import ProductCard from "../components/product/ProductCard";
import authAxios from "../utility/api";

import Spinner from "react-bootstrap/Spinner";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { fetchLatestProducts } from "../utility/api/product";
import { isAuthenticated } from "../utility/auth";
import { updateTokenIfExpired } from "../utility/auth";

const Home = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const parentCategories = useSelector((state) =>
    state.category.categories.filter((c) => c.parent === null)
  );

  useEffect(() => {
    const getProducts = async () => {
      const { data } = await fetchLatestProducts();
      setProducts(data.results);
      setLoading(false);
    };

    if (isAuthenticated()) {
      updateTokenIfExpired();
    }
    getProducts();
  }, []);

  const productCards = useMemo(() => {
    return products.map((product) => (
      <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
        <ProductCard product={product} />
      </Col>
    ));
  }, [products]);

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
        <Spinner />
      ) : (
        <>
          <Row xs={1} md={2} className="g-4">
            {productCards}
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
