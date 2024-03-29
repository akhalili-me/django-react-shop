import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";
import { setAlarm } from "../../alert/alarmSlice";
import { paymentSuccessfull } from "../../payment/paymentOperationsReducer";
import { clearAllItmesInCart } from "../../cart/cartReducers";
export const addOrder = createAsyncThunk(
  "orderOperations/addOrder",
  async (
    {
      addressId,
      totalPrice,
      shippingPrice,
      paymentMethod,
      orderItems,
      navigator,
    },
    { dispatch }
  ) => {
    try {
      const { data } = await authAxios.post(`/cart/orders/`, {
        address: addressId,
        total: totalPrice,
        shipping_price: shippingPrice,
        payment: { payment_method: paymentMethod },
        order_items: orderItems,
      });
      dispatch(clearAllItmesInCart());
      dispatch(
        setAlarm({
          message: "Order successfully added.",
          type: "success",
        })
      );

      // Just for testing
      dispatch(paymentSuccessfull({ paymentId: data.payment.id }));
      navigator(`/orders/${data.id}?paymentSuccess=true`);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

export const updateOrder = createAsyncThunk(
  "orderOperations/updateOrder",
  async ({ orderId, addressId, totalPrice, status }, { dispatch }) => {
    try {
      await authAxios.put(`/cart/orders/${orderId}`, {
        address: addressId,
        status: status,
        total: totalPrice,
      });
      dispatch(
        setAlarm({
          message: "Order successfully updated.",
          type: "success",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

export const deleteOrder = createAsyncThunk(
  "orderOperations/deleteOrder",
  async (id, { dispatch }) => {
    try {
      await authAxios.delete(`/cart/orders/${id}`);

      dispatch(
        setAlarm({
          message: "Order successfully deleted.",
          type: "success",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

// Order item crud
export const deleteOrderItem = createAsyncThunk(
  "orderItemOperations/deleteOrderItem",
  async (id, { dispatch }) => {
    try {
      await authAxios.delete(`/cart/orderitems/${id}`);

      dispatch(
        setAlarm({
          message: "orderItem succesfully deleted.",
          type: "success",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

export const updateOrderItem = createAsyncThunk(
  "orderItemOperations/updateOrderItem",
  async ({ id, orderId, productId, quantity }, { dispatch }) => {
    try {
      await authAxios.put(`/cart/orderitems/${id}`, {
        order: orderId,
        product: productId,
        quantity: quantity,
      });

      dispatch(
        setAlarm({
          message: "Order item successfuly updated.",
          type: "success",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

// Order payment crud
export const deleteOrderPayment = createAsyncThunk(
  "orderPaymentOperations/deleteOrderPayment",
  async (id, { dispatch }) => {
    try {
      await authAxios.delete(`/cart/payment/${id}`);
      dispatch(
        setAlarm({
          message: "Order payment successfuly deleted.",
          type: "success",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

export const updateOrderPayment = createAsyncThunk(
  "orderPayment/updateOrderPayment",
  async ({ id, amount, status }, { dispatch }) => {
    try {
      await authAxios.put(`/cart/payment/${id}`, {
        amount: amount,
        status: status,
      });

      dispatch(
        setAlarm({
          message: "Order payment successfuly updated.",
          type: "success",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);
