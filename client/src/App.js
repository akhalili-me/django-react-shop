import { BrowserRouter,Route,Routes,Navigate,useLocation} from "react-router-dom"
import Container from 'react-bootstrap/Container'

import Header from './components/Header'
import Footer from './components/Footer';
import Home from './pages/Home';
import Product from './pages/Product';
import ProductFilter from "./pages/ProductFilter";
import Login from "./pages/Login"
import Register from "./pages/Register"
import Profile from "./pages/Profile";
import Cart from "./pages/Cart";
import Alarm from "./components/common/Alarm";

import { isAuthenticated } from "./utility/auth";

function App() {

  function PrivateRoute({ component }) {
    const auth = isAuthenticated();
    const location = useLocation();
    return auth ? component : <Navigate to={`/login?back=${location.pathname}`} />;
  }

  return (
    <BrowserRouter >
      <Header/>
      <Alarm />
      <main className='py-3 main'>
        <Container>
          <Routes>

            <Route path="/" element={<Home />}/>
            <Route path="/product/:id" element={<Product />}/>
            <Route path="/product/filter/:id" element={<ProductFilter />}/>
            <Route path="/cart" element={<Cart />}/>
            <Route path="/login" element={isAuthenticated() ? <Navigate to={'/'} /> : <Login />}/>
            <Route path="/register" element={isAuthenticated() ? <Navigate to={'/'} /> : <Register />}/>
            
            {/* Protected Routes */}
            <Route path="/profile/*" element={<PrivateRoute component={<Profile />}/>}/>
          </Routes>
        </Container>
      </main>
     
      <Footer/>
    </BrowserRouter>
  );
}

export default App;
