import React from "react";
import { Table, Form } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { removeItemCart, updateItemCart } from "../../features/cart/cartSlice";
import { setAlarm } from "../../features/alert/alarmSlice";
const CartItems = ({ items }) => {
  const dispatch = useDispatch();

  const handleRemoveItem = (productId, index) => {
    dispatch(removeItemCart({ product: productId, index: index }));
  };

  const handleUpdateQuantity = (productId, productQuantity, event) => {
    const quantity = parseInt(event.target.value, 10);

    if (quantity >= Number(productQuantity)) {
      dispatch(setAlarm({ message: "No more in stock", type: "danger" }));
      return;
    }

    const data = {
      productId: productId,
      quantity: quantity,
    };
    dispatch(updateItemCart(data));
  };

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
        <td>
          <Form.Control
            onChange={(event) =>
              handleUpdateQuantity(i.product.id, i.product.quantity, event)
            }
            type="number"
            min={1}
            value={i.quantity}
            className="text-center"
          />
        </td>
        <td>
          <i
            onClick={() => handleRemoveItem(i.product.id, index)}
            class="fa-solid fa-xmark"
          ></i>
        </td>
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
          <th>Quantity</th>
          <th>#</th>
        </tr>
      </thead>
      <tbody>{products}</tbody>
    </Table>
  );
};

export default CartItems;
