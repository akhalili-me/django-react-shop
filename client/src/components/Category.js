import Card from 'react-bootstrap/Card';

const Category = () => {

  return (
    <a href='/'>
        <Card className='category'>
            <Card.Img variant="top" src="https://media.istockphoto.com/id/178716575/photo/mobile-devices.jpg?s=612x612&w=0&k=20&c=9YyINgAbcmjfY_HZe-i8FrLUS43-qZh6Sx6raIc_9vQ=" />
            <Card.Body className=''>
                <Card.Title className='text-center'><strong>Electronics</strong></Card.Title>
                {/* <Button variant="primary">Go somewhere</Button> */}
            </Card.Body>
        </Card>
    </a>
  );
}

export default Category;