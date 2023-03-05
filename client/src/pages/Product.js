import React,{useState,useEffect} from 'react'
import { useParams } from 'react-router-dom';
import axios from 'axios';

import ProductPage from '../components/ProductPage'
import Comment from '../components/Comment'

const Product = () => {
    const [product,setProduct] = useState([])
    const [comments,setComments] = useState([])

    const { id } = useParams();

    useEffect(() => {
        async function getProductInfo() {
            const [productResponse, commentsResponse] = await Promise.all([
                axios.get(`/products/${id}`),
                axios.get(`/products/${id}/comments`)
            ]);

            const { data: product } = productResponse;
            const { data: comments } = commentsResponse;

            setProduct(product)            
            setComments(comments)
        }
        
        getProductInfo()
    },[id])

 return (
    <>
        <ProductPage product={product}/>
        <h2 className='py-4'> Reviews</h2>
        <div className='comment_section'>
            <Comment comments={comments}/>
        </div>
    </>
  )
}

export default Product