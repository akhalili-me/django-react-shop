import React from 'react'
import {Table,Button,Col,Row,Form,ListGroup } from 'react-bootstrap';
import { useSelector, useDispatch } from 'react-redux'
import CartItems from '../components/CartItems';

const Cart = () => {
    const items = useSelector(state => state.cart.items)
    return (
        <>
            <h1 className='py-4'>Shopping Cart</h1>
            <Row>
                <Col md={9}>
                    <CartItems items={items}/>
                </Col>
                <Col md={3}>
                    <ListGroup className='checkout_sidebar' variant="">
                        <ListGroup.Item><span className='bold'>Items: </span> 3</ListGroup.Item>
                        <ListGroup.Item><span className='bold'>Total Price: </span> $500</ListGroup.Item>
                        <ListGroup.Item><Button variant="success">Checkout</Button></ListGroup.Item>
                    </ListGroup>    
                </Col>
            </Row>
            
          </>
        
    );
  };

export default Cart