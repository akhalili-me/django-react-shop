import React, { useEffect, useState } from "react";
import { Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { register } from "../features/auth/register/RegisterReducers";
import { clearRegisterErrors } from "../features/auth/register/RegisterSlice";

const Register = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const dispatch = useDispatch()
	const { loading, error,success} = useSelector(
		(state) => state.register
	);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (password !== passwordConfirm && password !== null) {
      setMessage("Passwords do not match!")
    } else {
      dispatch(register({email,username,password}))
    }
  };

  if (success === true) {
    navigate('/login');
  }
  
  useEffect(() => {
    dispatch(clearRegisterErrors())
  }, [dispatch])
  
  return (
    <div className="login_container center_screen">

      {message && <Message variant="danger" message={message}/>}
      {error && <Message variant="danger" message={error}/>}
      {loading && <Loader />}

      <h2 className="text-center">Register</h2>
      <Form onSubmit={handleSubmit} className="login_form">
        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-4">
          <Form.Label>Password confirm</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password confirm"
            name="password_confirm"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
          />
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          className="mx-auto d-grid gap-2 col-6"
        >
          Register
        </Button>
      </Form>
      <div className="text-center mt-4">
        Already a member? <Link to={"/login"}>Login</Link>{" "}
      </div>
    </div>
  );
};

export default Register;
