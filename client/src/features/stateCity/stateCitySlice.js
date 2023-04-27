import { createSlice } from "@reduxjs/toolkit";
import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const getLocations = createAsyncThunk(
  "location/getLocations",
  async () => {
    const { data } = await axios.get('/cart/location');
    return data;
  }
);

export const stateCitySlice = createSlice({
  name: "states",
  initialState: { states: [] },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getLocations.fulfilled, (state, action) => {
      state.states = action.payload;
    });
  },
});

export default stateCitySlice.reducer;
