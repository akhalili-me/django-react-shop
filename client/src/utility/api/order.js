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

export const addOrder = async (addressId,totalPrice,orderItems) => {
    try {
        await authAxios.post(`/cart/orders/`, {
            address: addressId,
            status: "created",
            total: totalPrice,
            order_items: orderItems,
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
export const deleteOrderItem = async (id) => {
    try {
        await authAxios.delete(`/cart/orderitems/${id}`);
    } catch (error) {
        throw new Error("failed to delete a order item, try again");
    }
};

export const updateOrderItem = async (id,orderId, productId, quantity) => {
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

//Payment CRUD
export const deletePayment = async (id) => {
    try {
        await authAxios.delete(`/cart/payment/${id}`);
    } catch (error) {
        throw new Error("failed to delete a payment, try again");
    }
};

export const updatePayment = async (id, amount, status) => {
    try {
        await authAxios.put(`/cart/payment/${id}`, {
            amount: amount,
            status: status,
        });
    } catch (error) {
        throw new Error("Failed to update payment, try again.");
    }
};
