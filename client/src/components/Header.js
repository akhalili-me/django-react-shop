import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

import { LinkContainer } from 'react-router-bootstrap'

import { isAuthenticated,logout } from '../utility/auth';

const header = () => {
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
              <Nav.Link><i className='fa-solid fa-cart-shopping'></i></Nav.Link>
            </LinkContainer>
            
            
            <NavDropdown id="navbarScrollingDropdown" title=<i class="fa-solid fa-user"></i> >
              <NavDropdown.Item href="#action3">Action</NavDropdown.Item>
              <NavDropdown.Item href="#action4">
                Another action
              </NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action5">
                Something else here
              </NavDropdown.Item>
            </NavDropdown>

            {  isAuthenticated() ? (
                  <Nav.Link onClick={logout}>Logout</Nav.Link>
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

export default header