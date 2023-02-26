import React from 'react'
import { useParams } from 'react-router-dom';

import ProductPage from '../components/ProductPage'
import Comment from '../components/Comment'
import products from '../products';

const Product = () => {
    const { id } = useParams();
    const product = products.find((p) => p._id===id)

    const sample_comments = [
        {
            'author': 'Amir khalili',
            'rate':3,
            'text':'Very good indeed'
        }
    ]
  return (
    <>
        <ProductPage product={product}/>

        <h2 className='py-4'> Reviews</h2>
        <div className='comment_section'>
            <Comment comments={sample_comments}/>
        </div>
    </>
  )
}

export default Product