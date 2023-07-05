import { combineReducers } from "@reduxjs/toolkit";
import cartReducer from "../features/cart/cartSlice";
import alarmReducer from "../features/alert/alarmSlice";
import categoryReducer from '../features/category/categorySlice'
import stateCityReducer from "../features/stateCity/stateCitySlice";
import productReducer from "../features/product/productSlice"
import productDetailsReducer from "../features/productDetails/ProductDetailSlice"
import authReducer from "../features/auth/authSlice"

const rootReducer = combineReducers({
  cart: cartReducer,
  alarm: alarmReducer,
  category: categoryReducer,
  location: stateCityReducer,
  product: productReducer,
  productDetails: productDetailsReducer,
  auth: authReducer
});

export default rootReducer;
