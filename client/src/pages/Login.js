import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import { Link, useSearchParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../components/common/Loader";
import Message from "../components/common/Message";
import { useEffect } from "react";
import { login } from "../features/auth/login/loginReducers";
import { clearLoginErrors } from "../features/auth/login/loginSlice";

const Login = () => {
	const [queryParams] = useSearchParams();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const dispatch = useDispatch();
	const { authenticated, loading, error} = useSelector(
		(state) => state.login
	);

	const register = useSelector(state => state.register)

	const handleSubmit = (event) => {
		event.preventDefault();
		dispatch(login({email, password}));
	};

	const redirectAfterLogin = () => {
		const back = queryParams.get("back");
		if (back) {
		  window.location.replace(back);
		} else {
		  window.location.replace("/");
		}
	};

	useEffect(() => {
		dispatch(clearLoginErrors())
		if (authenticated) {
			redirectAfterLogin();
		}
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [dispatch, authenticated]);

	return (
		<div className="login_container center_screen">
			{register.success && <Message variant={"success"} message={"Successfully registered, now login."} />}
			{error && <Message variant={"danger"} message={error} />}


			<h2 className="text-center">Login Page</h2>
			<Form onSubmit={handleSubmit} className="login_form">
				<Form.Group className="mb-3">
					<Form.Label>Email address</Form.Label>
					<Form.Control
						type="email"
						placeholder="Enter email"
						value={email}
						name="email"
						onChange={(e) => setEmail(e.target.value)}
					/>
				</Form.Group>

				<Form.Group className="mb-3" controlId="formBasicPassword">
					<Form.Label>Password</Form.Label>
					<Form.Control
						type="password"
						placeholder="Password"
						value={password}
						name="password"
						onChange={(e) => setPassword(e.target.value)}
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
					{loading ? <Loader /> : "Login"}
				</Button>
			</Form>
			<div className="text-center mt-4">
				Not a member? <Link to={"/register"}>Register</Link>{" "}
			</div>
		</div>
	);
};

export default Login;
