import { createSlice } from '@reduxjs/toolkit'
import { fetchCartItems } from '../../utility/cart'
import { addItemReducer, removeItemReducer } from './cartReducers'

export const cartSlice = createSlice({
  name: 'cart',
  initialState: { total:0, items:[] } ,
  reducers: {
    addItem: addItemReducer,
    removeItem: removeItemReducer,
    clearCart: state =>{
      state.items = [];
    },
    updateQuantity: (state,action) => {
    },
  },
  extraReducers: (builder) => {
    builder.addCase(fetchCartItems.fulfilled,(state,action) => {
      state.total = action.payload[0].total;
      state.items = action.payload[0].cart_items;
    })
  }
})

// Action creators are generated for each case reducer function
export const { addItem, removeItem, clearCart } = cartSlice.actions

export default cartSlice.reducer