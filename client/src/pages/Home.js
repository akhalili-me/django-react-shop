import React, { useEffect, useState,useCallback, useMemo} from 'react'
import Carousel from '../components/HomeSwiper'
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Category from "../components/Category";
import axios from 'axios';
import ProductCard from '../components/ProductCard';



const Home = () => {
    const [products,setProducts] = useState([])
    const [loading, setLoading] = useState(true)


    const fetchProducts = useCallback(async () =>{
        try {
            const { data } = await axios.get(`http://127.0.0.1:8000/products`)
            setProducts(data)
            setLoading(false);
        } catch (error) {
            console.error(error);
        }
 
    },[])

    useEffect(()=> {
        fetchProducts()
    },[fetchProducts])

    const productCards = useMemo(() => {
        return products.map((product) => (
          <Col key={product.id} sm={12} md={6} lg={4} xl={4}>
            <ProductCard product={product} />
          </Col>
        ));
      }, [products]);

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
            {products.map(product => (
                <Col key={product.id}  sm={4} md={4} lg={2} xl={2}>
                    <Category product={product} />
                </Col>
            ))}
        </Row>
    </div>
  )
}

export default Home