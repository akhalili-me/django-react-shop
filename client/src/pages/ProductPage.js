import React from 'react'
import {Col,Row,Button} from 'react-bootstrap'
import Form from 'react-bootstrap/Form';
import ListGroup from 'react-bootstrap/ListGroup'
import Carousel from 'react-bootstrap/Carousel';

import Rating from '../components/Rating'
const ProductPage = ({product}) => {
  return (
    <>
    <Row className=''>
        <Col md={6}>
        <Carousel interval={null} variant="dark">
            <Carousel.Item>
            <img className='rounded d-block w-100' alt='product-page' src='https://media.wired.com/photos/621980b1aaf30ea1c35e400a/191:100/w_2271,h_1189,c_limit/Gear-Samsung-S22-Series.jpg'/>
            </Carousel.Item>
            <Carousel.Item>
            <img className='rounded' alt='product-page' src='https://m-cdn.phonearena.com/images/phones/83157-350/Samsung-Galaxy-S22.jpg'/>
            </Carousel.Item>
 
        </Carousel>
        
        </Col>
        <Col md={6}>
            <h2 className='bold'>Sony Playstation 4 Pro White Version</h2>
            <hr/>
            <Row>
                <Col md={8}>
                <Rating value={3.5}/>
                <hr/>
                <div><strong>Price: $998.4</strong> </div>
                <hr/>
                <p><strong>Description:</strong> Introducing the iPhone 11 Pro. A transformative triple-camera system that adds tons of capability without complexity. An unprecedented leap in battery life',</p>
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
    <h2 className='py-4'> Reviews</h2>
    <div className='comment'>
    <h3>Amir Khalili</h3>
    <Rating value={4}/>
    <p>This was a really good product. thanks.
    </p>
    </div>
    <hr/>
    
    <div className='comment'>
    <h3>Reza Ahmadi</h3>
    <Rating value={1}/>
    <p>Very bad.
    </p>
    </div>
    <hr/>
    </>
  )
}

export default ProductPage