import React from 'react'
import {Col,Row,Button} from 'react-bootstrap'
import Form from 'react-bootstrap/Form';
import ListGroup from 'react-bootstrap/ListGroup'

import Carousel from './Carousel';
import Rating from '../components/Rating'


const ProductPage = ({product}) => {
    const images = [
        {
          'id': product._id,
          'name': product.name,
          'src': product.image,
        },
    ]

  return (
    <Row>
        <Col md={6}>
            <Carousel items={images} />
        </Col>

        <Col md={6}>
            <h2 className='bold line'>{product.name}</h2>
            <Row>
                <Col md={8} className='info_box_container'>
                    <div className='line'><Rating value={product.rating}/></div>
                    <div className='line'><strong>Price: ${product.price}</strong> </div>
                    <p><strong>Description:</strong> {product.description}</p>
                </Col>
                    
                <Col md={4} className='buy_box_container'>
                        <ListGroup >
                            <ListGroup.Item>Status: In Stock</ListGroup.Item>
                            <ListGroup.Item>      
                                <Form.Group className="" controlId="formBasicEmail">
                                    <Form.Control min={1} type="number" placeholder="Quantity" />
                                </Form.Group>
                            </ListGroup.Item>
                            <ListGroup.Item><Button variant="primary">Add to Cart</Button></ListGroup.Item>
                        </ListGroup>
                </Col>
            </Row>
        </Col>

    </Row>
  )
}

export default ProductPage