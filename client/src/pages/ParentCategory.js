import React, { useEffect, useMemo, useState } from "react";
import { useSelector } from "react-redux";
import { Navigate, useParams, useNavigate } from "react-router-dom";
import { fetchChildCategoriesWithTopSoldProducts } from "../utility/product";
import ProductCard from "../components/product/ProductCard";
import { Col } from "react-bootstrap";
const ParentCategory = () => {
  const { id } = useParams();
  const [parentCategory, setParentCategory] = useState();
  const [childCategoryProducts, setChildCategoryProducts] = useState();
  const categories = useSelector((state) => state.category.categories);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchChildCategories = async () => {
      try {
        const { data } = await fetchChildCategoriesWithTopSoldProducts(id);
        setChildCategoryProducts(data);
      } catch (error) {
        navigate("/notfound");
      }
    };
    setParentCategory(
      categories.find(
        (category) => category.parent === null && category.id === parseInt(id)
      )
    );
    fetchChildCategories();
  }, [id, navigate, categories]);

  return (
    <>
      <h1 className="py-3">{parentCategory?.name}</h1>
      {childCategoryProducts?.map((childCategory) => {
        return (
          <div key={childCategory.id}>
            <h2 className="py-3"><strong>{childCategory.name}</strong> top sold products</h2>
            {childCategory.products.map((product) => {
              return (
                <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                  <ProductCard product={product} />
                </Col>
              );
            })}
          </div>
        );
      })}
    </>
  );
};

export default ParentCategory;
