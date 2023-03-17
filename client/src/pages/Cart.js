import React from 'react'
import {Button,Col,Row,ListGroup } from 'react-bootstrap';
import { useSelector} from 'react-redux'
import CartItems from '../components/CartItems';

const Cart = () => {
    const cart = useSelector(state => state.cart)
    return (
        <>
            <h1 className='py-4'>Shopping Cart</h1>
            <Row>
                <Col md={9}>
                    <CartItems items={cart.items}/>
                </Col>
                <Col md={3}>
                    <ListGroup className='checkout_sidebar' variant="">
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