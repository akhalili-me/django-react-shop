import React from 'react'
import {Col,Row,Button} from 'react-bootstrap'
import Form from 'react-bootstrap/Form';
import ListGroup from 'react-bootstrap/ListGroup'

import Carousel from './Carousel';
import Rating from '../components/Rating'


const ProductPage = ({product}) => {
    const { _id, name, image, countInStock, price, rating, description } = product;
    const images = [
        {
          'id': _id,
          'name': name,
          'src': image,
        },
    ]
    

    const [status, product_price] = countInStock === 0 ? ['Out of Stock', 'Out of Stock'] : ['In Stock', price];


  return (
    <Row>
        <Col md={6}>
            <Carousel items={images} />
        </Col>

        <Col md={6}>
            <h2 className='bold line'>{name}</h2>
            <Row>
                <Col md={8} className='info_box_container'>
                    <div className='line'><Rating value={rating}/></div>
                    <div className='line'><strong>Price: {product_price}</strong> </div>
                    <p><strong>Description:</strong> {description}</p>
                </Col>
                    
                <Col md={4} className='buy_box_container'>
                <ListGroup className='text-center'>
                    <ListGroup.Item key="status">{status}</ListGroup.Item>
                    {countInStock > 0 && (
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