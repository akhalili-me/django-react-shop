import { isAuthenticated } from "../../utility/auth";
import authAxios from "../../utility/api";

export const addItemReducer = (state, action) => {
  const { id, name, price, images, quantity } = action.payload;
  const existingItem = state.items.find(i => i.product.id === id);

  if (quantity === 0) {
    throw new Error('Not available in stock')
  } else if (existingItem) {
    throw new Error('Already available in cart')
  }

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
  
  if (isAuthenticated()) {
    addOrUpdateItemInDatabase(id,1)
  }

  calculateTotal(state)
};

export const removeItemReducer = (state,action) => {
  const itemIndex = action.payload.index
  const productId = action.payload.product
  state.items.splice(itemIndex,1)
  calculateTotal(state)

  if (isAuthenticated()) {
    removeItemInDatabase(productId)
  }
}

export const UpdateItemQuantityReducer = (state,action) => {
  const { productId, quantity } = action.payload;

  const existingItem = state.items.find(i => i.product.id === productId);
  existingItem.quantity = quantity

  if (isAuthenticated()) {
    addOrUpdateItemInDatabase(productId,quantity)
  }
  calculateTotal(state)
}

export const clearAllItmesReducer = (state,action) =>{
  state.total = 0
  state.items=[]

  if (isAuthenticated()) {
    removeAllItemsInDatabase()
  }
}

const calculateTotal = (state) => {
  state.total = state.items.reduce( 
    (total, item) => total + item.product.price * item.quantity,
    0
  );
}

const removeAllItemsInDatabase = async () => {
  await authAxios.delete('cart/removeall')
}

const removeItemInDatabase = async (id) => {
  await authAxios.delete(`cart/${id}`)
}

const addOrUpdateItemInDatabase = async (id,quantity) => {
  await authAxios.post('/cart/create',{
    product: id,
    quantity: quantity
  })
}

