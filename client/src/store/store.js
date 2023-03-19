import { configureStore } from '@reduxjs/toolkit'
import cartReducer from '../features/cart/cartSlice'
import alarmReducer from '../features/alert/alarmSlice'

export default configureStore({
  reducer: {
    cart: cartReducer,
    alarm: alarmReducer,
  },
})
