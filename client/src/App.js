import {
  BrowserRouter,
  Route,
  Routes,
  Navigate,
  useLocation,
} from "react-router-dom";
import Container from "react-bootstrap/Container";
import { useEffect } from "react";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Product from "./pages/Product";
import ProductFilter from "./pages/ProductFilter";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Cart from "./pages/Cart";
import Alarm from "./components/common/Alarm";
import ParentCategory from "./pages/ParentCategory";
import { useDispatch, useSelector } from "react-redux";
import NotFound from "./pages/NotFound";
import Checkout from "./pages/Checkout";
import { getCategories } from "./features/category/categorySlice";
import { refreshAndSetAccessToken } from "./features/auth/token/tokenReducers";
import OrderDetails from "./components/profile/order/OrderDetails";
import { getCartItems } from "./features/cart/cartOperations";
import ProductSearch from "./pages/ProductSearch";

function App() {
  const dispatch = useDispatch();
  const {authenticated} = useSelector(state => state.login)

  useEffect(() => {
    dispatch(getCategories());
  }, [dispatch])
  
  useEffect(() => {
    if (authenticated) {
      dispatch(refreshAndSetAccessToken())
      dispatch(getCartItems())
      
      const interval = setInterval( () => {
        dispatch(refreshAndSetAccessToken())},
        10 * 60 * 1000
      );

      return () => {
        clearInterval(interval);
      };
    }
  }, [dispatch,authenticated]);

  function PrivateRoute({ component }) {
    const location = useLocation();
    return authenticated ? (
      component
    ) : (
      <Navigate to={`/login?back=${location.pathname}`} />
    );
  }

  return (
    <BrowserRouter>
      <Header />
      <Alarm />
      <main className="py-3 main">
        <Container>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/product/:id/*" element={<Product />} />
            <Route path="/product/filter/:id" element={<ProductFilter />} />
            <Route path="/product/search/:q" element={<ProductSearch />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/category/:id" element={<ParentCategory />} />
            <Route
              path="/login"
              element={authenticated ? <Navigate to={"/"} /> : <Login />}
            />
            <Route
              path="/register"
              element={authenticated ? <Navigate to={"/"} /> : <Register />}
            />

            {/* Protected Routes */}
            <Route
              path="/orders/:id"
              element={<PrivateRoute component={<OrderDetails />} />}
            />

            <Route
              path="/profile/*"
              element={<PrivateRoute component={<Profile />} />}
            />
            <Route
              path="/checkout"
              element={<PrivateRoute component={<Checkout />} />}
            />
        

            {/* NotFound */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Container>
      </main>

      <Footer />
    </BrowserRouter>
  );
}

export default App;
