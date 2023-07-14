import React, { useEffect } from "react";
import Table from "react-bootstrap/Table";
import { useDispatch, useSelector } from "react-bootstrap";
import { getProductFeatures } from "../../features/product/productFeatures/productFeaturesReducers";
import Loader from "../common/Loader";
import Message from "../common/Message";

const Features = ({ productId }) => {
  const dispatch = useDispatch();
  const { features, loading, error } = useSelector(
    (state) => state.productFeatures
  );

  useEffect(() => {
    dispatch(getProductFeatures(productId));
  }, [dispatch, productId]);

  return (
    <>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant={"danger"} message={error} />
      ) : (
        <Table striped className="mt-4">
          <tbody>
            {features.map((feature) => (
              <tr>
                <td>{feature.name}</td>
                <td>{feature.description}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </>
  );
};

export default Features;
