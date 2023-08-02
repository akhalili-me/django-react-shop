import { isAuthenticated } from "../../utility/token";
import {
  addOrUpdateItemInDatabase,
  removeAllItemsInDatabase,
  removeItemInDatabase,
} from "./cartOperations";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { setAlarm } from "../alert/alarmSlice";

export const addItemToCart = createAsyncThunk(
  "cart/addItem",
  async ({ item }, thunkAPI) => {
    const { dispatch } = thunkAPI;
    try {
      if (item.quantity === 0) {
        throw new Error("Not available in stock");
      }

      if (isItemExist(thunkAPI.getState().cart.items, item.id)) {
        throw new Error("Already available in cart");
      }
      if (isAuthenticated()) {
        await addOrUpdateItemInDatabase(item.id, 1);
      }
      dispatch(
        setAlarm({ message: "successfully added to cart", type: "success" })
      );
      return item;
    } catch (error) {
      dispatch(setAlarm({ message: error.message, type: "danger" }));
      throw new Error(error);
    }
  }
);

export const removeItemFromCart = createAsyncThunk(
  "cart/removeItem",
  async ({ product, index }, { dispatch }) => {
    try {
      if (isAuthenticated()) {
        await removeItemInDatabase(product);
      }

      dispatch(
        setAlarm({ message: "successfully removed from cart", type: "success" })
      );

      return index;
    } catch (error) {
      dispatch(setAlarm({ message: error.message, type: "danger" }));
      throw new Error(error);
    }
  }
);

export const UpdateItemQuantityInCart = createAsyncThunk(
  "cart/updateItem",
  async ({ productId, quantity }, { dispatch }) => {
    try {
      if (isAuthenticated()) {
        await addOrUpdateItemInDatabase(productId, quantity);
      }

      dispatch(
        setAlarm({
          message: "successfully updated the quantity.",
          type: "success",
        })
      );

      return { productId, quantity };
    } catch (error) {
      dispatch(setAlarm({ message: error.message, type: "danger" }));
      throw new Error(error);
    }
  }
);

export const clearAllItmesInCart = createAsyncThunk(
  "cart/removeAllItem",
  async (_, { dispatch }) => {
    try {
      if (isAuthenticated()) {
        await removeAllItemsInDatabase();
      }
      dispatch(
        setAlarm({ message: "successfully emptied the cart", type: "success" })
      );
    } catch (error) {
      dispatch(setAlarm({ message: error.message, type: "danger" }));
      throw new Error(error);
    }
  }
);

// ##############################
// ##############################

// State changing functions
export const removeItemFromState = (state, index) => {
  state.items.splice(index, 1);
  calculateTotal(state);
};

export const addItemToState = (state, item) => {
  const serializedItem = serializeItemData(item);
  state.items.push(serializedItem);
  calculateTotal(state);
};

export const UpdateItemQuantityInState = (state, payload) => {
  const { productId, quantity } = payload;
  const existingItem = state.items.find((i) => i.product.id === productId);
  existingItem.quantity = quantity;
  calculateTotal(state);
};

// Utility cart functions
const isItemExist = (items, id) => {
  const item = items.find((i) => i.product.id === id);
  return true ? item : false;
};

const serializeItemData = (product) => {
  const { id, name, price, images, quantity } = product;
  return {
    product: {
      id: id,
      image: images?.[0],
      name: name,
      price: price,
      quantity: quantity,
    },
    quantity: 1,
  };
};

const calculateTotal = (state) => {
  state.total = state.items.reduce(
    (total, item) => total + item.product.price * item.quantity,
    0
  );
};
