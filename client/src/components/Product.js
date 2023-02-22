import React from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import {truncateString} from '../utility/string_utils'

const Product = ({product}) => {
  return (
    <Card className="h-100">
      <a href='/'>
      <Card.Img variant="top" src={product.image} />
      </a>
      <Card.Body>
        <Card.Title>
          <strong>{product.name}</strong>
        </Card.Title>
        <Card.Text className='description'>
          {truncateString(product.description)}
        </Card.Text>
        <Card.Text as='h3'>
        ${product.price}
        </Card.Text>
        <span className='reviews-number'><i class="fa-solid fa-comment"></i>47</span>
        <span className='rating-number' ><i class="fa-solid fa-star"></i>4.4</span>
        <Button variant="light"><i class="fa-solid fa-cart-shopping"></i></Button>
      </Card.Body>
    </Card>
  )
}

export default Product