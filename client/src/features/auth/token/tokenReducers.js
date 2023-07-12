import { createAsyncThunk } from "@reduxjs/toolkit";
import { setAccessTokenLocalStorage,isTokenExpired,getRefreshToken,removeJWTTokensLocalStorage} from "../../../utility/token";
import { logout } from "../login/loginSlice";
import axios from "axios";


export const refreshAndSetAccessToken = createAsyncThunk(
    "token/refreshAccessToken",
    async (_, { dispatch }) => {
      try {
        const refToken = getRefreshToken();
  
        if (!refToken || isTokenExpired(refToken)) {
          dispatch(logout());
          throw new Error("Login session expired. Login again.");
        }
  
        const { data } = await axios.post("/accounts/token/refresh", {
          refresh: refToken,
        });
        setAccessTokenLocalStorage(data.access);
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message;
        throw new Error(errorMessage);
      }
    }
  );
  
