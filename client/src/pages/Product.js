import React,{useState,useEffect} from 'react'
import { useParams } from 'react-router-dom';
import axios from 'axios';

import ProductPage from '../components/product/ProductPage'
import Reviews from '../components/product/Reviews'

const Product = () => {
    const [product,setProduct] = useState([])
    const { id } = useParams();

    useEffect(() => {
        async function getProducts() {
            const response = await axios.get(`/products/${id}/`)
            const { data: product } = response;
            setProduct(product)            
        }
        
        getProducts()
    },[id])

 return (
    <>
        <ProductPage product={product}/>
        <h2 className='py-4'> Reviews</h2>
        <div className='comment_section'>
            <Reviews productId={id}/>
        </div>
    </>
  )
}

export default Product