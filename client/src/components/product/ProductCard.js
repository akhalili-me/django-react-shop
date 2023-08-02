import Button from "react-bootstrap/Button";
import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";

import { truncateString } from "../../utility/string_utils";
import { addItemToCart } from "../../features/cart/cartReducers";


const ProductCard = ({ product }) => {
  const dispatch = useDispatch();
  
  const handleAddToCart = () => {
    dispatch(addItemToCart({ item: product }));
  };

  return (
    <>
      <Card className="h-100">
        <Link to={`/product/${product.id}`}>
          <Card.Img variant="top" src={product.images[0]?.image} />
        </Link>
        <Card.Body>
          <Card.Title>
            <strong>{product.name}</strong>
          </Card.Title>
          <Card.Text className="description">
            {truncateString(product.description)}
          </Card.Text>
          <Card.Text as="h3">${product.price}</Card.Text>
          <span className="reviews-number">
            <i class="fa-solid fa-comment"></i>
            {product.num_comments}
          </span>
          <span>
            <i class="fa-solid fa-star star_color"></i>
            {product.rate}
          </span>
          <Button onClick={() => handleAddToCart()} variant="light">
            <i class="fa-solid fa-cart-shopping"></i>
          </Button>
        </Card.Body>
      </Card>
    </>
  );
};

export default ProductCard;
