import { useState } from 'react'
import Button from 'react-bootstrap/Button';
import {Card,Alert} from 'react-bootstrap';
import {Link} from 'react-router-dom'
import { useDispatch } from 'react-redux'

import {truncateString} from '../utility/string_utils'
import { addItem } from '../features/cart/cartSlice';

const ProductCard = ({product}) => {
  const [showAlert, setShowAlert] = useState(false);
  const [alertMsg, setAlertMsg] = useState('');
  const [alertVariant, setAlertVariant] = useState('');
  const dispatch = useDispatch()

  const handleAddToCart = () => {

    try {
      dispatch(addItem(product))
      setAlertVariant('success')
      setAlertMsg('Successfully added to cart!')
    } catch (error) {
      console.log();
      setAlertVariant('danger')
      setAlertMsg(error.message)
    } finally {
      setShowAlert(true);
      setTimeout(() => setShowAlert(false), 2000);
    }
  }
  
  return (
    <>
    <Card className="h-100">

      {showAlert && (
          <Alert className='success_alert text-center' variant={alertVariant}>
              {alertMsg}
          </Alert>
      )}
 
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
        <Button onClick={() => handleAddToCart()} variant="light"><i class="fa-solid fa-cart-shopping"></i></Button>
   
      </Card.Body>
    </Card>
    </>
  )
}

export default ProductCard