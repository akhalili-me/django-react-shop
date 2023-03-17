import { isAuthenticated } from "../../utility/auth";
import authAxios from "../../utility/api";

export const addItemReducer = (state, action) => {
  const { id, name, price, images, quantity } = action.payload;
  const existingItem = state.items.find(i => i.product.id === id);
  let finalQuantity = 1

  if (existingItem) {
    existingItem.quantity += 1;
    finalQuantity = existingItem.quantity
  } else {
    const serializedItem = {
      product: {
        id: id,
        image: images?.[0],
        name: name, 
        price: price, 
        quantity: quantity
      },
      quantity: 1
    };
    state.items.push(serializedItem);
  }
  
  if (isAuthenticated()) {
    updateItemInDatabase(id,finalQuantity)
  }

  state.total = state.items.reduce( 
    (total, item) => total + item.product.price * item.quantity,
    0
  );
};

export const removeItemReducer = (state,action) => {
  const itemIndex = action.payload.index
  const productId = action.payload.product
  state.items.splice(itemIndex,1)

  if (isAuthenticated()) {
    removeItemInDatabase(productId)
  }
}


const removeItemInDatabase = async (id) => {
  await authAxios.delete(`cart/${id}`)
}

const updateItemInDatabase = async (id,quantity) => {
  await authAxios.post('/cart/create',{
    product: id,
    quantity: quantity
  })
}