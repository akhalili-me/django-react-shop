import { createSlice } from "@reduxjs/toolkit";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { fetchCategories } from "../../utility/category";

export const getCategories = createAsyncThunk(
  "category/getCategories",
  async () => {
    const { data } = await fetchCategories();
    return data;
  }
);

export const categorySlice = createSlice({
  name: "category",
  initialState: { categories: [] },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getCategories.fulfilled, (state, action) => {
      state.categories = action.payload;
    });
  },
});

export default categorySlice.reducer;
