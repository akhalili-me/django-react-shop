import React from 'react'
import products from '../products'
import Carousel from '../components/Carousel'
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Product from '../components/Product';
import Category from "../components/Category";

const Home = () => {
  return (
    <div>
        <Carousel/>
        <h1 className='py-4' >Latest Products</h1>
        <Row xs={1} md={2} className="g-4">
            {products.map(product => (
                <Col key={product._id}  sm={12} md={6} lg={4} xl={4}>
                    <Product product={product} />
                </Col>
            ))}
        </Row>
        <h1 className='py-4' >Categories</h1>     
        <Row xs={1} md={2} className="">
            {products.map(product => (
                <Col key={product._id}  sm={4} md={4} lg={2} xl={2}>
                    <Category product={product} />
                </Col>
            ))}
        </Row>
    </div>
  )
}

export default Home