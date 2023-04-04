import axios from "axios";

export const fetchCategories = async () => {
  try {
    const response = await axios.get("/products/categories");
    return response;
  } catch (error) {
    throw new Error('Failed to fetch categories.')
  }
};

