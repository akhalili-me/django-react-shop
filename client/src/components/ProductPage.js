import React from 'react'
import {Col,Row,Button} from 'react-bootstrap'
import Form from 'react-bootstrap/Form';
import ListGroup from 'react-bootstrap/ListGroup'
import { useSelector, useDispatch } from 'react-redux'

import Carousel from './Carousel';
import Rating from '../components/Rating'
import { addItem } from '../features/cart/cartSlice';

const ProductPage = ({product}) => {
    const {name, quantity, price, rate, description, images } = product;
    const [status, product_price] = quantity === 0 ? ['Out of Stock', 'Out of Stock'] : ['In Stock', price];
    const dispatch = useDispatch()

  return (
    <Row>
        <Col md={6}>
            <Carousel items={images} />
        </Col>

        <Col md={6}>
            <h2 className='bold line'>{name}</h2>
            <Row>
                <Col md={8} className='info_box_container'>
                    <div className='line'><Rating value={rate}/></div>
                    <div className='line'><strong>Price: {product_price}</strong> </div>
                    <p><strong>Description:</strong> {description}</p>
                </Col>
                    
                <Col md={4} className='buy_box_container'>
                <ListGroup className='text-center'>
                    <ListGroup.Item key="status">{status}</ListGroup.Item>
                    {quantity > 0 && (
                        <>
                        <ListGroup.Item key="quantity">
                            <Form.Group controlId="formBasicEmail">
                            <Form.Control min={1} type="number" placeholder="Quantity" />
                            </Form.Group>
                        </ListGroup.Item>
                        <ListGroup.Item key="add-to-cart">
                            <Button variant="primary">Add to Cart</Button>
                        </ListGroup.Item>
                        </>
                    )}
                </ListGroup>    
                </Col>
            </Row>
        </Col>
    </Row>
  )
}

export default ProductPage;