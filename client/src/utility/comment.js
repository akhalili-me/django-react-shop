import authAxios from "./api";

export const fetchComments = async (productId) => {
    try {
        const response = await authAxios.get(`/products/${productId}/comments`)
        return response
    } catch (error) {
        throw new Error(error.response.data)
    }
}


export const addComment = async (comment,productId) => {
    try {
        await authAxios.post(`/products/${productId}/comments`,{
            text: comment.text,
            rate: comment.rate
        })
    } catch (error) {
        throw new Error(error.response.data)
    }
}