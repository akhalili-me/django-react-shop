import React from 'react'
import { Col,Row } from 'react-bootstrap'
import Filter from '../components/Filter'

const ProductFilter = () => {
  return (
    <Row>
        <Col md={9}>
        </Col>
        <Col md={3}>
            <Filter/>
        </Col>
    </Row>
  )
}

export default ProductFilter