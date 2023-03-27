import authAxios from "./api";
import { isAuthenticated } from "./auth";

export const fetchProductComments = async (productId) => {
  try {
    const response = await authAxios.get(`/products/${productId}/comments`);
    return response;
  } catch (error) {
    throw new Error("Fetch product comments failed, reload.");
  }
};

export const addComment = async (comment, productId) => {
  try {
    await authAxios.post(`/products/${productId}/comments/create`, {
      text: comment.text,
      rate: comment.rate,
    });
  } catch (error) {
    throw new Error("Submit comment failed, try again.");
  }
};

export const fetchUserComments = async () => {
  try {
    const response = await authAxios.get("/accounts/comments");
    return response;
  } catch (error) {
    throw new Error("Fetch user comments failed, reload.");
  }
};

export const retrieveComment = async (id) => {
  try {
    const response = await authAxios.get(`/accounts/comments/${id}`);
    return response;
  } catch (error) {
    throw new Error("Retrieve Comment Failed, try again.");
  }
};

export const DeleteComment = async (id) => {
  try {
    await authAxios.delete(`/accounts/comments/${id}`);
  } catch (error) {
    throw new Error("Delete Comment Failed, try again.");
  }
};

export const updateComment = async (comment) => {
  try {
    await authAxios.put(`/accounts/comments/${comment.id}`, {
      text: comment.text,
      rate: comment.rate,
    });
  } catch (error) {
    throw new Error("Edit Comment Failed, try again.");
  }
};

export const likeComment = async (commentId) => {
  if (isAuthenticated() === false) {
    throw new Error("Please login to like comments.");
  }

  try {
    await authAxios.post(`/accounts/comments/${commentId}/like/`, {});
  } catch (error) {
    throw new Error("Like Comment Failed, try again.");
  }
};

export const removeLikeComment = async (commentId) => {
  try {
    await authAxios.delete(`/accounts/comments/${commentId}/like/remove`);
  } catch (error) {
    throw new Error("Remove like Comment Failed, try again.");
  }
};
