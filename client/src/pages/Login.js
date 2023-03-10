import React, {useState } from 'react';
import { Form, Button, Col, Row } from 'react-bootstrap';
import { Link,useSearchParams } from 'react-router-dom';
import { login } from '../utility/auth';
import Alert from 'react-bootstrap/Alert';

const Login = () => {
  const [queryParams] = useSearchParams();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [failedLogin, setFailedLogin] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const register = queryParams.get('register') || false

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    login(email, password)
      .then((response) => {
        if (response.status !== 200) {
          setFailedLogin(true);
        } else {
          setIsLoggedIn(true);
        }
      })
      .catch((error) => {
        setFailedLogin(true);
      });
  };

  const error = (
    <Alert variant={'danger'}>
      Sorry, we could not find your account.
    </Alert>
  );

  const registerSuccess = (
    <Alert variant={'success'}>
      You were successfuly registered. Now login.
    </Alert>
  )

  if (isLoggedIn) {
    const back = queryParams.get('back')
    if (back) {
      window.location.replace(back)
    } else{
      window.location.reload()
    }
  }

  return (
    <div className="login_container center_screen">
      {register ? registerSuccess : ''}
      {failedLogin ? error : ''}
      <h2 className="text-center">Login Page</h2>
      <Form onSubmit={handleSubmit} className="login_form">
        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={handleEmailChange}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            onChange={handlePasswordChange}
          />
        </Form.Group>
        <Row className="mb-4 m-1">
          <Col md={6}>
            <Form.Check type="checkbox" label="Remeber Me" />
          </Col>
          <Col md={6}>
            <Link to={``}>Forgot Password?</Link>
          </Col>
        </Row>
        <Button
          variant="primary"
          type="submit"
          className="mx-auto d-grid gap-2 col-6"
        >
          Login
        </Button>
      </Form>
      <div className="text-center mt-4">
        Not a member? <Link to={'/register'}>Register</Link>{' '}
      </div>
    </div>
  );
};

export default Login;
