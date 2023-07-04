import { createSlice } from "@reduxjs/toolkit";
import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const getCategories = createAsyncThunk(
	"category/getCategories",
	async () => {
		try {
			const { data } = await axios.get("/products/categories");
			return data;
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const categorySlice = createSlice({
	name: "category",
	initialState: { categories: [], loading: null, error: "" },
	reducers: {},
	extraReducers: (builder) => {
		builder
			.addCase(getCategories.pending, (state) => {
				state.loading = true;
			})
			.addCase(getCategories.fulfilled, (state, action) => {
				state.loading = false;
				state.categories = action.payload;
			})
			.addCase(getCategories.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			});
	},
});

export default categorySlice.reducer;
