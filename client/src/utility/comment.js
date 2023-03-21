import authAxios from "./api";
import axios from "axios";

export const fetchProductComments = async (productId) => {
    try {
        const response = await axios.get(`/products/${productId}/comments`)
        return response
    } catch (error) {
        throw new Error('Fetch product comments failed, reload.')
    }
}

export const addComment = async (comment,productId) => {
    try {
        await authAxios.post(`/products/${productId}/comments`,{
            text: comment.text,
            rate: comment.rate
        })
    } catch (error) {
        throw new Error('Submit comment failed, try again.')
    }
}

export const fetchUserComments = async () => {
    try {
        const response = authAxios.get('/accounts/comments')
        return response
    } catch (error) {
        throw new Error('Fetch user comments failed, reload.')
    }
}

export const retrieveComment = async (id) => {
    try {
        const response = authAxios.get(`/accounts/comments/${id}`)
        return response
    } catch (error) {
        throw new Error('Retrieve Comment Failed, try again.')
    }
}

export const DeleteComment = async (id) => {
    try {
        authAxios.delete(`/accounts/comments/${id}`)
    } catch (error) {
        throw new Error('Delete Comment Failed, try again.')
    }
}

export const updateComment = async (comment) => {
    try {
        authAxios.put(`/accounts/comments/${comment.id}`,{
            text: comment.text,
            rate: comment.rate
        })
    } catch (error) {
        throw new Error('Edit Comment Failed, try again.')
    }
}



