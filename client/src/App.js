import { BrowserRouter as Router,Route,Routes,Navigate} from "react-router-dom"
import Container from 'react-bootstrap/Container'

import Header from './components/Header'
import Footer from './components/Footer';
import Home from './pages/Home';
import Product from './pages/Product';
import ProductFilter from "./pages/ProductFilter";
import Login from "./pages/Login"
import Register from "./pages/Register"
import { isAuthenticated } from "./utility/auth";


function App() {
  return (
    <Router >
      <Header/>
      
      <main className='py-3 main'>
        <Container>
          <Routes>

            <Route path="/" element={<Home />}/>

            <Route path="/product/:id" element={<Product />}/>
            <Route path="/product/filter/:id" element={<ProductFilter />}/>

            <Route path="/login" element={isAuthenticated() ? <Navigate to={'/'} /> : <Login />}/>
            <Route path="/register" element={isAuthenticated() ? <Navigate to={'/'} /> : <Register />}/>

            {/* <Route element={<ProtectedRoutes auth={isAuth}/>}>
              <Route path='/dashboard' element={<Dashboard />} />
              <Route path='/availablechitplans' element={<AvailableChitPlans/>}/>
              <Route path='/notifications' element={<Notifications/>}/>
              <Route path='/chitplaninfo' element={<ChitPlanInfo/>}/>
              <Route path='/payment' element={<PaymentPage />}/>
            </Route> */}
          </Routes>
        </Container>
      </main>
     
      <Footer/>
    </Router>
  );
}

export default App;
