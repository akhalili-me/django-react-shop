import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import Alert from 'react-bootstrap/Alert';
import { register } from '../utility/auth';
import { jsonErrorstoString } from '../utility/string_utils';

const Register = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [failed, setFailed] = useState(false);
    const [error, setError] = useState('');


    const handleFieldChange = (event) => {
        const target = event.target;
        const value = target.value
        const name = target.name

        switch (name) {
            case 'email':
                setEmail(value)
                break;
            case 'username':
                setUsername(value)
                break;
            case 'password':
                setPassword(value)
                break;
            case 'password_confirm':
                setPasswordConfirm(value)
                break;
            default:
                break;
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        
        if (password !== passwordConfirm && password !== null) {
            setError('Password and Password Confirm must be same.')
            setFailed(true)
        } else{
            register(email,username,password).then(response =>{
                if (response.status !== 201) {
                    setError(jsonErrorstoString(response.data))
                    setFailed(true)
                } else{
                    window.location.replace('login?register=true')
                }
            })
        }
    }

  return (
    <div className='login_container center_screen'>
        {failed ? (
        <Alert variant={'danger'}>
            {error}
        </Alert>): ''}

        <h2 className='text-center'>Register</h2>
        <Form onSubmit={handleSubmit} className='login_form' >
            <Form.Group className='mb-3'>
                <Form.Label>Email address</Form.Label>
                <Form.Control type="email" placeholder="Enter email" name='email' value={email} onChange={handleFieldChange} />
            </Form.Group>

            <Form.Group className='mb-3'>
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" placeholder="Enter username" name='username' value={username} onChange={handleFieldChange} />
            </Form.Group>

            <Form.Group className='mb-3'>
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" name='password' value={password} onChange={handleFieldChange} />
            </Form.Group>

            <Form.Group className='mb-4'>
                <Form.Label>Password confirm</Form.Label>
                <Form.Control type="password" placeholder="Password confirm" name='password_confirm' value={passwordConfirm} onChange={handleFieldChange} />
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