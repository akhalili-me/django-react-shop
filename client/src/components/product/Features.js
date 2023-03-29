import React, { useState, useEffect } from "react";
import Table from "react-bootstrap/Table";
import { fetchProductFeatures } from "../../utility/product";

const Features = ({ productId }) => {
  const [features, setFeatures] = useState([]);

  useEffect(() => {
    const getFeatures = async () => {
      const { data } = await fetchProductFeatures(productId);
      setFeatures(data);
    };

    getFeatures();
  }, [productId]);

  return (
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
  );
};

export default Features;
