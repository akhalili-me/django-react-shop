import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { Link, useSearchParams } from "react-router-dom";
import { login } from "../utility/auth";
import Alert from "react-bootstrap/Alert";
import { useDispatch } from "react-redux";
import { fetchCartItems } from "../features/cart/cartSlice";

const Login = () => {
  const [queryParams] = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [failedLogin, setFailedLogin] = useState(false);
  const dispatch = useDispatch();

  const registerSuccess = queryParams.get("register") || false;

  const handleFieldChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;

    switch (name) {
      case "email":
        setEmail(value);
        break;
      case "password":
        setPassword(value);
        break;
      default:
        break;
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    login(email, password)
      .then((response) => {
        if (response.status !== 200) {
          setFailedLogin(true);
        } else {
          dispatch(fetchCartItems())
            .then(() => {
              redirectAfterLogin();
            })
            .catch((error) => {
              console.error(error);
            });
        }
      })
      .catch((error) => {
        setFailedLogin(true);
      });
  };

  const redirectAfterLogin = () => {
    const back = queryParams.get("back");
    if (back) {
      window.location.replace(back);
    } else {
      window.location.replace("/");
    }
  };

  const errorAlert = (
    <Alert variant={"danger"}>Sorry, login failed. Try again.</Alert>
  );

  const registerSuccessAlert = (
    <Alert variant={"success"}>
      You were successfuly registered. Now login.
    </Alert>
  );

  return (
    <div className="login_container center_screen">
      {registerSuccess ? registerSuccessAlert : ""}
      {failedLogin ? errorAlert : ""}
      <h2 className="text-center">Login Page</h2>
      <Form onSubmit={handleSubmit} className="login_form">
        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            value={email}
            name="email"
            onChange={handleFieldChange}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            name="password"
            onChange={handleFieldChange}
          />
        </Form.Group>
        <div className="mb-4 m-1">
          <Link to={``}>Forgot Password?</Link>
        </div>
        <Button
          variant="primary"
          type="submit"
          className="mx-auto d-grid gap-2 col-6"
        >
          Login
        </Button>
      </Form>
      <div className="text-center mt-4">
        Not a member? <Link to={"/register"}>Register</Link>{" "}
      </div>
    </div>
  );
};

export default Login;
