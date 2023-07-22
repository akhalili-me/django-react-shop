import React from "react";
import { Table } from "react-bootstrap";

const OrderItems = ({ items }) => {
  
  const renderImage = (item) => {
    if (item.product.image) {
      return (
        <img
          className="rounded"
          alt={item.product.image.name}
          src={item.product.image.image}
        />
      );
    } else if (item.product.images && item.product.images.length > 0) {
      return (
        <img
          className="rounded"
          alt={item.product.images[0].name}
          src={item.product.images[0].image}
        />
      );
    } else {
      return <span>Image not available</span>;
    }
  };

  const renderProducts = () => {
    if (!items || items.length === 0) {
      return (
        <tr>
          <td colSpan={4}>No items in the order.</td>
        </tr>
      );
    }

    return items.map((item, index) => (
      <tr key={index} className="align-middle">
        <td>{renderImage(item)}</td>
        <td>{item.product.name}</td>
        <td>${item.product.price}</td>
        <td>{item.quantity}</td>
      </tr>
    ));
  };

  return (
    <Table className="cart_table text-center" striped bordered hover>
      <thead>
        <tr>
          <th>Product Image</th>
          <th>Product</th>
          <th>Price</th>
          <th>Quantity</th>
        </tr>
      </thead>
      <tbody>{renderProducts()}</tbody>
    </Table>
  );
};

export default OrderItems;
