import React from 'react'
import {Table,Form} from 'react-bootstrap';
import { useDispatch } from 'react-redux';
import { removeItem } from '../features/cart/cartSlice';

const CartItems = ({items}) => {
    const dispatch = useDispatch()

    const handleRemoveItem = (productId,index) => {
        dispatch(removeItem({product:productId,index:index}))
    }

    const products = items.map((i,index) => {
        return(
        <tr class="align-middle" >
            <td>{i.product.image ? <img className='rounded' alt={i.product.image.name} src={i.product.image.image}/> : 'Image not Available'}</td>
            <td>{i.product.name}</td>
            <td>${i.product.price}</td>
            <td> <Form.Control type="number" min="1" defaultValue={i.quantity} className="text-center" /></td>
            <td>
            <i onClick={() => handleRemoveItem(i.product.id,index)} class="fa-solid fa-xmark"></i>
            </td>
        </tr>
    )})

  return (
    <Table className='cart_table text-center' striped bordered hover>
        <thead>
            <tr>
                <th>Product Image</th>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>#</th>
            </tr>
        </thead>
        <tbody>
            {products}
        </tbody>
    </Table>
  )
}

export default CartItems