import { combineReducers } from "@reduxjs/toolkit";
import cartReducer from "../features/cart/cartSlice";
import alarmReducer from "../features/alert/alarmSlice";
import categoryReducer from '../features/category/categorySlice'
import stateCityReducer from "../features/stateCity/stateCitySlice";
const rootReducer = combineReducers({
  cart: cartReducer,
  alarm: alarmReducer,
  category: categoryReducer,
  location: stateCityReducer
});

export default rootReducer;
