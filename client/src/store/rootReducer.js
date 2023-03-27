import { combineReducers } from "@reduxjs/toolkit";
import cartReducer from "../features/cart/cartSlice";
import alarmReducer from "../features/alert/alarmSlice";

const rootReducer = combineReducers({
  cart: cartReducer,
  alarm: alarmReducer,
});

export default rootReducer;
