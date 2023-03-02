import { BrowserRouter as Router,Route,Routes} from "react-router-dom"
import Container from 'react-bootstrap/Container'

import Header from './components/Header'
import Footer from './components/Footer';
import Home from './pages/Home';
import Product from './pages/Product';
import ProductFilter from "./pages/ProductFilter";

function App() {
  return (
    <Router >
      <Header/>
      
      <main className='py-3 main'>
        <Container>
          <Routes>

            <Route path="/" element={<Home />}/>
            <Route path="/product/:id" element={<Product />}/>
            <Route path="/product/filter" element={<ProductFilter />}/>

          </Routes>
        </Container>
      </main>
     
      <Footer/>
    </Router>
  );
}

export default App;
