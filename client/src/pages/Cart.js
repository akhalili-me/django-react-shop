import React from 'react'
import {Button,Col,Row,ListGroup } from 'react-bootstrap';
import { useSelector,useDispatch} from 'react-redux'
import CartItems from '../components/cart/CartItems';
import { clearCart } from '../features/cart/cartSlice';

const Cart = () => {
    const cart = useSelector(state => state.cart)
    const dispatch = useDispatch()

    const handleClearCart = () => {
        dispatch(clearCart())
    }

    return (
        <>
            <h1 className='py-3'>Shopping Cart <Button onClick={() => handleClearCart()} variant='danger' >Clear Cart</Button></h1> 
            <Row>
                <Col md={9}>
                    <CartItems items={cart.items}/>
                </Col>
                <Col md={3}>
                    <ListGroup className='checkout_sidebar'>
                        <ListGroup.Item><span className='bold'>Items: </span> {cart.items.length}</ListGroup.Item>
                        <ListGroup.Item><span className='bold'>Total Price: </span> ${cart.total}</ListGroup.Item>
                        <ListGroup.Item><Button variant="success">Checkout</Button></ListGroup.Item>
                    </ListGroup>    
                </Col>
            </Row>
          </>
    );
  };

export default Cart