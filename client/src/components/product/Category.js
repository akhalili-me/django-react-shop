import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';

const Category = ({category}) => {

  return (
    <Link to={`/product/filter/${category.id}`}>
        <Card className='category'>
            <Card.Img variant="top" src={category.image} />
            <Card.Body className=''>
                <Card.Title className='text-center'><strong>{category.name}</strong></Card.Title>
            </Card.Body>
        </Card>
    </Link>
  );
}

export default Category;