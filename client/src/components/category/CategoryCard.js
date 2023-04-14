import Card from "react-bootstrap/Card";
import { Link } from "react-router-dom";

const Category = ({ category }) => {
  return (
      <Card className="category">
        <Card.Img variant="top" src={category.image} />
        <Card.Body className="">
          <Card.Title className="text-center">
            <strong>{category.name}</strong>
          </Card.Title>
        </Card.Body>
      </Card>
  );
};

export default Category;
