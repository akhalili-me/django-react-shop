import axios from "axios";

export const fetchLatestProducts = async () => {
    try {
        const response = await axios.get('/products/')
        return response
    } catch (error) {
        throw new Error("Failed to fetch products, try again.");
    }
}


export const fetchProductFeatures = async (productId) => {
  try {
    const response = await axios.get(`/products/${productId}/features`);
    return response;
  } catch (error) {
    throw new Error("Failed to fetch product features, try again.");
  }
};

export const fetchChildCategoriesWithTopSoldProducts = async (parentCategoryId) => {
  try {
    const response = await axios.get(`/products/category/${parentCategoryId}`);
    return response;
  } catch (error) {
    throw new Error("Failed to fetch products, try again.");
  }
}