import authAxios from "../api";

// Orders CRUD operation
export const fetchUserOrders = async () => {
    try {
        const response = await authAxios.get(`/cart/orders`);
        return response;
    } catch (error) {
        throw new Error("Fetch user orders failed, try again.");
    }
};

export const addOrder = async (addressId, totalPrice) => {
    try {
        await authAxios.post(`/cart/orders`, {
            address: addressId,
            status: "created",
            total: totalPrice,
        });
    } catch (error) {
        throw new Error("Failed to submit new order, try again.");
    }
};

export const deleteOrder = async (id) => {
    try {
        await authAxios.delete(`/cart/orders/${id}`);
    } catch (error) {
        throw new Error("Failed to delete a order, try again.");
    }
};

export const updateOrder = async (orderId, addressId, totalPrice, status) => {
    try {
        await authAxios.put(`/cart/orders/${orderId}`, {
            address: addressId,
            status: status,
            total: totalPrice,
        });
    } catch (error) {
        throw new Error("Fetch user orders failed, try again.");
    }
};

// Order items CRUD
export const fetchOrderItems = async (orderId) => {
    try {
        const response = await authAxios.get(
            `/cart/orderitemsbyorderid/${orderId}`
        );
        return response;
    } catch (error) {
        throw new Error("Fetch order items failed, reload.");
    }
};

export const addOrderItem = async (orderId, productId, quantity) => {
    try {
        await authAxios.post(`/cart/orderitems`, {
            order: orderId,
            product: productId,
            quantity: quantity,
        });
    } catch (error) {
        throw new Error("Failed to create order item, try again.");
    }
};

export const deleteOrderItems = async (id) => {
    try {
        await authAxios.delete(`/cart/orderitems/${id}`);
    } catch (error) {
        throw new Error("failed to delete a order item, try again");
    }
};

export const updateOrderItems = async (id,orderId, productId, quantity) => {
    try {
        await authAxios.put(`/cart/orderitems/${id}`,{
            order: orderId,
            product: productId,
            quantity: quantity,
        });
    } catch (error) {
        throw new Error("Failed to update order item, try again.");
    }
};
