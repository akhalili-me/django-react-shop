import { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Badge from 'react-bootstrap/Badge';
import { LinkContainer } from 'react-router-bootstrap'
import { useSelector } from 'react-redux';

import { isAuthenticated,logout } from '../utility/auth';

const Header = () => {
  const [cartBadge, setCartBadge] = useState(0);
  const cartItemCount = useSelector((state) => state.cart.items.length)

  useEffect(() => {
    setCartBadge(cartItemCount)
  },[cartItemCount])

  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <LinkContainer to={'/'}>
          <Navbar.Brand>E-Shop</Navbar.Brand>
        </LinkContainer>
        
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '100px' }}
            navbarScroll
          >
            <LinkContainer to={'cart'}>
              <Nav.Link><i className='fa-solid fa-cart-shopping'></i><Badge className='cart_badge' bg="dark">{cartBadge}</Badge></Nav.Link>
            </LinkContainer>
            
            {  isAuthenticated() ? (
                <>
                  <NavDropdown id="navbarScrollingDropdown" title=<i class="fa-solid fa-user"></i> >

                    <LinkContainer to={'/profile'}>
                      <NavDropdown.Item>Amir Khalili</NavDropdown.Item>
                    </LinkContainer>
                    
                    <NavDropdown.Divider />
                    <LinkContainer to={'/profile/orders'}>
                      <NavDropdown.Item>Orders</NavDropdown.Item>
                    </LinkContainer>
                    <LinkContainer to={'/profile/comments'}>
                      <NavDropdown.Item>Comments</NavDropdown.Item>
                    </LinkContainer>
               
                  </NavDropdown>
                  <Nav.Link onClick={logout}>Logout</Nav.Link>
                </>
              ):(
                <LinkContainer to={'login'}>
                 <Nav.Link>Login</Nav.Link>
                </LinkContainer>
              )
            }

            
            <LinkContainer to={'categories'}>
              <Nav.Link>Categories</Nav.Link>
            </LinkContainer>

          </Nav>
          <Form className="d-flex">
            <Form.Control
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
            />
            <Button variant="outline-success">Search</Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default Header