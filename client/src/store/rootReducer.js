import { combineReducers } from "@reduxjs/toolkit";
import cartReducer from "../features/cart/cartSlice";
import alarmReducer from "../features/alert/alarmSlice";
import categoryReducer from '../features/category/categorySlice'
import stateCityReducer from "../features/stateCity/stateCitySlice";
import productListReducer from "../features/product/productList/productListSlice"
import productDetailsReducer from "../features/product/productDetails/ProductDetailSlice"
import registerReducers from "../features/auth/register/RegisterSlice"
import loginReducers from "../features/auth/login/loginSlice"
import commentListReducer from "../features/comment/commentsList/commentsListSlice"
import commentDetailsReducer from "../features/comment/commentDetails/commentDetailsSlice"
import commentOperationsReducer from "../features/comment/commentOperations/commentOperationsSlice"
import addressListReducers from "../features/address/addressList/addressListSlice"
import addressDetailsReducers from "../features/address/addressDetails/addressDetailsSlice"
import addressOperationsReducers from "../features/address/addressOperations/addressOperationsSlice"

const rootReducer = combineReducers({
  cart: cartReducer,
  alarm: alarmReducer,
  category: categoryReducer,
  location: stateCityReducer,

  // auth
  login: loginReducers,
  register: registerReducers,

  // Products
  productList: productListReducer,
  productDetails: productDetailsReducer,
  
  // Comments
  commentList: commentListReducer,
  commentDetails:commentDetailsReducer ,
  commentOperations : commentOperationsReducer,

  // Addreeses 
  addressList: addressListReducers,
  addressDetails: addressDetailsReducers,
  addressOperations: addressOperationsReducers,
});

export default rootReducer;
