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

    if (isAuthenticated()) {
      addOrUpdateItemInDatabase(item.id, 1);
    }

    const serializedItem = serializeItemData(item);
    state.items.push(serializedItem);

    calculateTotal(state);
};

export const removeItemReducer = (state, action) => {
    const { product, index } = action.payload;

    if (isAuthenticated()) {
        removeItemInDatabase(product);
    }

    state.items.splice(index, 1);
    calculateTotal(state);
};

export const UpdateItemQuantityReducer = (state, action) => {
  const { productId, quantity } = action.payload;

  if (isAuthenticated()) {
      addOrUpdateItemInDatabase(productId, quantity);
  }

  const existingItem = state.items.find((i) => i.product.id === productId);
  existingItem.quantity = quantity;
  calculateTotal(state);
};

export const clearAllItmesReducer = (state, action) => {
  if (isAuthenticated()) {
    removeAllItemsInDatabase();
  }
  state.total = 0;
  state.items = [];
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
    try {
        await authAxios.delete("cart/removeall");
    } catch (error) {
      throw new Error("Failed to remove items, try again.");
    }
}

const removeItemInDatabase = async (id) => {
  try {
    await authAxios.delete(`cart/${id}`);
  } catch (error) {
    throw new Error("Failed to remove item, try again.");
  }
};

const addOrUpdateItemInDatabase = async (id, quantity) => {
  try {
    await authAxios.post("/cart/create", {
      product: id,
      quantity: quantity,
    });
  } catch (error) {
    throw new Error("Failed to add, try again.");
  }
};
