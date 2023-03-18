import React from 'react'
import {Col,Row,Button} from 'react-bootstrap'
import ListGroup from 'react-bootstrap/ListGroup'
import {useDispatch } from 'react-redux'
import { LinkContainer } from 'react-router-bootstrap'

import Carousel from './Carousel';
import Rating from '../components/Rating'
import { addItem } from '../features/cart/cartSlice';

const ProductPage = ({product}) => {
    const {name, quantity, price, rate, description, images } = product;
    const [status, product_price] = quantity === 0 ? ['Out of Stock', 'Out of Stock'] : ['In Stock', price];
    const dispatch = useDispatch()

    const handleAddToCart = () => {
        try {
        dispatch(addItem(product))
            
        } catch (error) {
        }
    }

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
                        <ListGroup.Item key="add-to-cart">
                            <LinkContainer to={'/cart'}>
                                <Button onClick={() => handleAddToCart()} variant="primary">Add to Cart</Button>
                            </LinkContainer>
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