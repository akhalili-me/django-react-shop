import React from 'react'
import { useSelector, useDispatch } from "react-redux";

const Checkout = () => {
    const cart = useSelector((state) => state.cart);
    const dispatch = useDispatch();
  return (

    <>
    <h1>Choose your address</h1>
    <h1>Checkout</h1>
    </>
  )
}

export default Checkout