import { combineReducers } from "@reduxjs/toolkit";
import cartReducer from "../features/cart/cartSlice";
import alarmReducer from "../features/alert/alarmSlice";
import categoryReducer from '../features/category/categorySlice'
import stateCityReducer from "../features/stateCity/stateCitySlice";
import productListReducer from "../features/product/productList/productListSlice"
import productDetailsReducer from "../features/product/productDetails/ProductDetailSlice"
import authReducer from "../features/auth/authSlice"
import commentListReducer from "../features/comment/commentsList/commentsListSlice"
import commentDetailsReducer from "../features/comment/commentDetails/commentDetailsSlice"
import commentOperationsReducer from "../features/comment/commentOperations/commentOperationsSlice"

const rootReducer = combineReducers({
  cart: cartReducer,
  alarm: alarmReducer,
  category: categoryReducer,
  location: stateCityReducer,
  auth: authReducer,

  // Products
  productList: productListReducer,
  productDetails: productDetailsReducer,
  
  // Comments
  commentList: commentListReducer,
  commentDetails:commentDetailsReducer ,
  commentOperations : commentOperationsReducer
});

export default rootReducer;
