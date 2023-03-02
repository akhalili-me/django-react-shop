import React from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import {Link} from 'react-router-dom'

import {truncateString} from '../utility/string_utils'

const ProductCard = ({product}) => {
  return (
    <Card className="h-100">
      <Link to={`/product/${product.id}`}>
      <Card.Img variant="top" src={product.image} />
      </Link>
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
        <span className='reviews-number'><i class="fa-solid fa-comment"></i>{product.num_comments}</span>
        <span><i class="fa-solid fa-star star_color"></i>{product.rate}</span>
        <Button variant="light"><i class="fa-solid fa-cart-shopping"></i></Button>
      </Card.Body>
    </Card>
  )
}

export default ProductCard