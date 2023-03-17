import React, { useEffect, useState,useCallback, useMemo} from 'react'
import Carousel from '../components/HomeSwiper'
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Category from "../components/Category";
import axios from 'axios';
import ProductCard from '../components/ProductCard';
import authAxios from '../utility/api';

import { isAuthenticated } from '../utility/auth';

import { useDispatch } from 'react-redux';
import { fetchCartItems } from '../utility/cart';
import { updateTokenIfExpired } from '../utility/auth';

const Home = () => {
    const [products,setProducts] = useState([])
    const [categories,setCategories] = useState([])
    const [loading, setLoading] = useState(true)
    const dispatch = useDispatch();

    const fetchProducts = useCallback(async () =>{
        try {
            const { data } = await axios.get("/products/")
            setProducts(data)
            setLoading(false);
        } catch (error) {
            console.error(error);
        }
 
    },[])

    const fetchCategories = useCallback(async () =>{
        try {
            const { data } = await authAxios.get(`/products/categories/`)
            setCategories(data)
        } catch (error) {
            console.error(error);
        }
 
    },[])


    useEffect(()=> {
        if (isAuthenticated()) {
          updateTokenIfExpired()
          dispatch(fetchCartItems())
        }
        fetchProducts()
        fetchCategories()
    },[fetchProducts,fetchCategories,dispatch])

    const productCards = useMemo(() => {
        return products.map((product) => (
          <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
            <ProductCard product={product} />
          </Col>
        ));
      }, [products]);


    const categoryCards = useMemo(() => {
        return categories.map((category) => (
          <Col key={category.id} sm={4} md={4} lg={2} xl={2}>
            <Category category={category} />
          </Col>
        ));
      }, [categories]);



  return (
    <div>
        <Carousel/>
        <h1 className='py-4' >Latest Products</h1>

        {loading ? <h4>Loading...</h4>: ( 
            <>
            <Row xs={1} md={2} className="g-4">
                {productCards}
            </Row>
            <a className=''>See More...</a>
            </>

        )}
 
        <h1 className='py-4' >Categories</h1>     
        <Row xs={1} md={2} className="">
            {categoryCards}
        </Row>
    </div>
  )
}

export default Home