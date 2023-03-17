import authAxios from '../utility/api'
import { createAsyncThunk } from '@reduxjs/toolkit';

export const fetchCartItems = createAsyncThunk(
  'cart/fetchCartItems',
  async () => {
    const response = await authAxios.get('/cart');
    return response.data;
  }
);
