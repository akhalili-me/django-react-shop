import { isAuthenticated } from "../../utility/auth";
import authAxios from "../../utility/api";

export const addItemReducer = (state, action) => {
  const item = action.payload;

  if (item.quantity === 0) {
    throw new Error("Not available in stock");
  }

  if (isItemExist(state.items, item.id)) {
    throw new Error("Already available in cart");
  }

  const serializedItem = serializeItemData(item);
  state.items.push(serializedItem);

  if (isAuthenticated()) {
    addOrUpdateItemInDatabase(item.id, 1);
  }

  calculateTotal(state);
};

export const removeItemReducer = (state, action) => {
  const { product, index } = action.payload;
  state.items.splice(index, 1);
  calculateTotal(state);

  if (isAuthenticated()) {
    removeItemInDatabase(product);
  }
};

export const UpdateItemQuantityReducer = (state, action) => {
  const { productId, quantity } = action.payload;

  const existingItem = state.items.find((i) => i.product.id === productId);
  existingItem.quantity = quantity;

  if (isAuthenticated()) {
    addOrUpdateItemInDatabase(productId, quantity);
  }
  calculateTotal(state);
};

export const clearAllItmesReducer = (state, action) => {
  state.total = 0;
  state.items = [];

  if (isAuthenticated()) {
    removeAllItemsInDatabase();
  }
};

// ##############################
// ##############################

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

const removeAllItemsInDatabase = async () => {
  await authAxios.delete("cart/removeall");
};

const removeItemInDatabase = async (id) => {
  await authAxios.delete(`cart/${id}`);
};

const addOrUpdateItemInDatabase = async (id, quantity) => {
  await authAxios.post("/cart/create", {
    product: id,
    quantity: quantity,
  });
};
