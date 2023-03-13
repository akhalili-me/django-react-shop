import React from 'react'
import {Table,Button,Col,Row,Form,ListGroup } from 'react-bootstrap';


const Cart = ({ cartItems, handleRemoveItem }) => {
    return (
        <>
            <h1 className='py-4'>Shopping Cart</h1>
            <Row>
                <Col md={9}>
                    <Table className='cart_table text-center' striped bordered hover>
                        <thead>
                        <tr>
                            <th>Product Image</th>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody>
                            <tr class="align-middle" >
                                <td><img className='rounded' alt='' src='https://redstore.am/uploads/shop/products/large/ffed713345a629513f80ca6ffb978947.jpg'/></td>
                                <td>Iphone 11</td>
                                <td>$55.99</td>
                                <td> <Form.Control type="number" min="1" defaultValue={1} className="text-center" /></td>
                                <td>
                                <i class="fa-solid fa-xmark"></i>
                                </td>
                            </tr>
                        </tbody>
                    </Table>
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