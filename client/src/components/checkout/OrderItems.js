import React from 'react'
import { Table } from "react-bootstrap";

const OrderItems = ({ items }) => {

    const products = items.map((i, index) => {
      return (
        <tr class="align-middle">
          <td>
            {i.product.image ? (
              <img
                className="rounded"
                alt={i.product.image.name}
                src={i.product.image.image}
              />
            ) : (
              "Image not available"
            )}
          </td>
          <td>{i.product.name}</td>
          <td>${i.product.price}</td>
        </tr>
      );
    });
  
    return (
      <Table className="cart_table text-center" striped bordered hover>
        <thead>
          <tr>
            <th>Product Image</th>
            <th>Product</th>
            <th>Price</th>
          </tr>
        </thead>
        <tbody>{products}</tbody>
      </Table>
    );
}

export default OrderItems