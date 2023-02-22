import Header from './components/Header'
import Footer from './components/Footer';
import Container from 'react-bootstrap/Container'
import Home from './pages/Home';

function App() {
  return (
    <div >
      <Header/>
      
      <main className='py-3'>
        <Container>
          <Home/>
          {/* Myapp */}
        </Container>
      </main>
     
      <Footer/>
      <script src="https://cdn.jsdelivr.net/npm/swiper@9/swiper-element-bundle.min.js"></script>
    </div>
    
  );
}

export default App;
