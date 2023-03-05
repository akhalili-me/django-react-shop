import React, { useEffect, useState, useMemo } from "react";
import { Col, Row } from "react-bootstrap";
import Filter from "../components/Filter";
import axios from "axios";
import ProductCard from "../components/ProductCard";
import { useParams} from "react-router-dom";
import { useSearchParams } from 'react-router-dom'

const ProductFilter = () => {
  const [products, setProducts] = useState([]);
  const [queryParams] = useSearchParams();
  const { id } = useParams();
  

  useEffect(() => {
    let params = ''
    const baseURL = `/products/search/${id}?`;
  
    const min = queryParams.get("min") || 0;
    const max = queryParams.get("max")|| 0;
    const sort = queryParams.get("sort") || 'default';
    const has_selling_stock = queryParams.get("has_selling_stock") || false;
    
    if (min !== 0 ) {
      params += `min=${min}&`
    }
  
    if (max !== 0) {
      params += `max=${max}&`
    }
  
    if (sort !== 'default') {
      params += `sort=${sort}&`
    }

    if (has_selling_stock !== false) {
      params += `has_selling_stock=${has_selling_stock}&`
    }

    const fetchProducts = async () => {
      const finalURL = baseURL + params

      const { data } = await axios.get(finalURL);
      setProducts(data.results);
    };
  
    fetchProducts();
  }, [id, queryParams]);
  

  const productCards = useMemo(
    () =>
      products.map((product) => (
        <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
          <ProductCard product={product} />
        </Col>
      )),
    [products]
  );

  return (
    <Row>
      <Col md={9}>
        <Row xs={1} md={2} className="g-4">
          {productCards}
        </Row>
      </Col>
      <Col md={3}>
        <Filter />
      </Col>
    </Row>
  );
};

export default ProductFilter;
