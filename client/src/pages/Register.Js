import React, { useState } from 'react';
import { Form, Button,Col,Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Register = () => {
  return (
    <div className='login_container center_screen'>
        <h2 className='text-center'>Register</h2>
        <Form className='login_form' >
            <Form.Group className='mb-3'>
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email"  />
            </Form.Group>

            <Form.Group className='mb-3'>
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Enter username"  />
            </Form.Group>

            <Form.Group className='mb-3' controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" />
            </Form.Group>

            <Form.Group className='mb-4' controlId="formBasicPassword">
                <Form.Label>Password confirm</Form.Label>
                <Form.Control type="password" placeholder="Password confirm" />
            </Form.Group>

            <Button variant="primary" type="submit" className='mx-auto d-grid gap-2 col-6'>
                Register
            </Button>
        </Form>
      <div className='text-center mt-4'>Already a member? <Link to={'/login'}>Login</Link> </div> 
    </div>
  )
}

export default Register