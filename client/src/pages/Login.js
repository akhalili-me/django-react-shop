import React, { useState } from 'react';
import { Form, Button,Col,Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';


const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(`Email: ${email}, Password: ${password}`);
  };

  return (
    <div className='login_container center_screen'>
      <h2 className='text-center'>Login Page</h2>
      <Form onSubmit={handleSubmit} className='login_form' >
        <Form.Group className='mb-3'>
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" value={email} onChange={handleEmailChange} />
        </Form.Group>

        <Form.Group className='mb-3' controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" value={password} onChange={handlePasswordChange} />
        </Form.Group>
        <Row className='mb-4 m-1'>
          <Col md={6}>
            <Form.Check 
              type='checkbox'
              label='Remeber Me'
            />
          </Col>
          <Col  md={6} >
            <Link to={``}>Forgot Password?</Link>
          </Col>
        </Row>
        <Button variant="primary" type="submit" className='mx-auto d-grid gap-2 col-6'>
          Login
        </Button>
      </Form>
      <div className='text-center mt-4'>Not a member? <Link to={'/register'}>Register</Link> </div> 
    </div>
  )
}

export default Login