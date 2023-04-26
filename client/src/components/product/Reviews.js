import { useEffect, useState, useCallback } from "react";
import Rating from "../common/Rating";
import { isAuthenticated } from "../../utility/auth";
import CommentForm from "./CommentForm";
import { fetchProductComments } from "../../utility/api/comment";
import { Link } from "react-router-dom";
import LikeComment from "../common/LikeComment";
import Pagination from "../common/Pagination";
import { useSearchParams } from "react-router-dom";

const Reviews = ({ productId }) => {
  const [comments, setComments] = useState([]);
  const [commentCount, setcommentCount] = useState(0);
  const [queryParams] = useSearchParams();

  const page = queryParams.get("page") || 1;

  const getComments = useCallback(async () => {
    const { data } = await fetchProductComments(productId,page);
    setComments(data.results);
    setcommentCount(data.count);
  }, [productId,page]);

  useEffect(() => {
    getComments();
  }, [getComments]);

  return (
    <div className="py-4">
      {isAuthenticated() ? (
        <CommentForm productId={productId} getComments={getComments} />
      ) : (
        <h2 className="bold mb-4">
          <Link to={"/login"}>Login </Link>
          to Comment
        </h2>
      )}
      <div>
        {comments.map((comment) => (
          <div className="comment line">
            <h3>{comment.author}</h3>
            <Rating
              value={comment.rate}
              text={<LikeComment comment={comment} getComments={getComments} />}
            />
            <p>{comment.text}</p>
          </div>
        ))}
      </div>

      <Pagination count={commentCount} paginateBy={4} />
    </div>
  );
};

export default Reviews;
