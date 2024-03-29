import { useEffect, useState } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { clearAllItmesInCart } from "../features/cart/cartReducers";
import { logout } from "../features/auth/login/loginSlice";
import {
  Offcanvas,
  Nav,
  Navbar,
  Badge,
  NavDropdown,
  Form,
  Button,
  Container,
} from "react-bootstrap";
import CategorySidebar from "./category/CategorySidebar";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const [cartBadge, setCartBadge] = useState(0);
  const cartItemCount = useSelector((state) => state.cart.items?.length);
  const { authenticated } = useSelector((state) => state.login);
  const [showCategories, setShowCategories] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    setCartBadge(cartItemCount);
  }, [cartItemCount]);

  const handleLogout = async () => {
    dispatch(logout());
    dispatch(clearAllItmesInCart());
  };

  const handleSearchProducts = (e) => {
    e.preventDefault();
    const q = e.target.elements.search.value;
    navigate(`/product/search/${q}`);
  };

  const handleCloseCategories = () => setShowCategories(false);
  const handleShowCategories = () => setShowCategories(true);

  return (
    <>
      <Offcanvas show={showCategories} onHide={handleCloseCategories}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Product Categories</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <CategorySidebar closeSidebar={handleCloseCategories} />
        </Offcanvas.Body>
      </Offcanvas>

      <Navbar bg="light" expand="lg">
        <Container>
          <LinkContainer to={"/"}>
            <Navbar.Brand>E-Shop</Navbar.Brand>
          </LinkContainer>

          <Navbar.Toggle aria-controls="navbarScroll" />
          <Navbar.Collapse id="navbarScroll">
            <Nav
              className="me-auto my-2 my-lg-0"
              style={{ maxHeight: "100px" }}
              navbarScroll
            >
              <LinkContainer to={"cart"}>
                <Nav.Link>
                  <i className="fa-solid fa-cart-shopping"></i>
                  <Badge className="cart_badge" bg="dark">
                    {cartBadge}
                  </Badge>
                </Nav.Link>
              </LinkContainer>

              {authenticated ? (
                <>
                  <NavDropdown
                    id="navbarScrollingDropdown"
                    title=<i class="fa-solid fa-user"></i>
                  >
                    <LinkContainer to={"/profile"}>
                      <NavDropdown.Item>Amir Khalili</NavDropdown.Item>
                    </LinkContainer>

                    <NavDropdown.Divider />
                    <LinkContainer to={"/profile/orders"}>
                      <NavDropdown.Item>Orders</NavDropdown.Item>
                    </LinkContainer>
                    <LinkContainer to={"/profile/comments"}>
                      <NavDropdown.Item>Comments</NavDropdown.Item>
                    </LinkContainer>
                  </NavDropdown>
                  <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
                </>
              ) : (
                <LinkContainer to={"login"}>
                  <Nav.Link>Login</Nav.Link>
                </LinkContainer>
              )}

              <Nav.Link onClick={handleShowCategories}>Categories</Nav.Link>
            </Nav>
            <Form className="d-flex" onSubmit={handleSearchProducts}>
              <Form.Control
                type="search"
                name="search"
                placeholder="Search"
                className="me-2"
                aria-label="Search"
              />
              <Button type="submit" variant="outline-success">
                Search
              </Button>
            </Form>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </>
  );
};

export default Header;
