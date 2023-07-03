import axios from "axios";
import { createAsyncThunk } from "@reduxjs/toolkit";

export const getLatestProducts = createAsyncThunk(
	"product/latestProducts",
	async () => {
		try {
			const { data } = await axios.get("/products/");
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

export const getProductsByFilter = createAsyncThunk("product/filterProducts",async(childCategoryId,urlParams) => {
    try {
        const URL = `/products/search/${childCategoryId}?${urlParams}`;
        const { data } = axios.get(URL);
        return data
    } catch (error) {
        const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
    }
})

export const getChildCategoriesWithTopSoldProducts = createAsyncThunk("product/filterProducts",async(childCategoryId,urlParams) => {
    try {
        const URL = `/products/search/${childCategoryId}?${urlParams}`;
        const { data } = axios.get(URL);
        return data
    } catch (error) {
        const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
    }
})