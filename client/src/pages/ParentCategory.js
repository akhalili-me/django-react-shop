import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams, useNavigate } from "react-router-dom";
import ProductCard from "../components/product/ProductCard";
import { Col } from "react-bootstrap";
import { getChildCategoriesWithTopSoldProducts } from "../features/product/childCategoryProducts/childCategoryProductsReducers";
import Loader from "../components/common/Loader"
import Message from "../components/common/Message"

const ParentCategory = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const categories = useSelector((state) => state.category.categories);
  const navigate = useNavigate();

  const { childCategory, parentCategory, loading, error } = useSelector(
    (state) => state.childCategoryProducts
  );

  useEffect(() => {

    if (categories.length > 0) {
      const category = categories.find((category) => category.id === Number(id))
      if (!category || category.parent !== null) {
        navigate("/notfound");
      }
    }

    dispatch(getChildCategoriesWithTopSoldProducts({ parentCategoryId: id }));
  }, [id, dispatch,categories,navigate]);

  return (
    <>
      <h1 className="py-3">{parentCategory}</h1>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        childCategory?.map((childCategory) => {
          return (
            <div key={childCategory.id}>
              <h2 className="py-3">
                <strong>{childCategory.name}</strong> top sold products
              </h2>
              {childCategory.products.map((product) => {
                return (
                  <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
                    <ProductCard product={product} />
                  </Col>
                );
              })}
            </div>
          );
        })
      )}
      {}
    </>
  );
};

export default ParentCategory;
