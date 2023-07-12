import { useEffect} from "react";
import Rating from "../common/Rating";
import CommentForm from "./CommentForm";
import { Link } from "react-router-dom";
import LikeComment from "../common/LikeComment";
import Pagination from "../common/Pagination";
import { useSearchParams } from "react-router-dom";
import { getProductComments } from "../../features/comment/commentsList/commentsListReducers";
import { useDispatch,useSelector } from "react-redux";
import Loader from "../common/Loader";
import Message from "../common/Message";

const Comments = ({ productId }) => {
  const dispatch = useDispatch()
  const [queryParams] = useSearchParams();
  const page = queryParams.get("page") || 1;

  const {authenticated} = useSelector(state => state.login)
  const { comments, loading, error, count } = useSelector(
    (state) => state.commentList
  );

  useEffect(() => {
    dispatch(getProductComments({ productId, page }));
  }, [dispatch,page,productId]);

  return (
    <div className="py-4">
      {authenticated ? (
        <CommentForm productId={productId} />
      ) : (
        <h2 className="bold mb-4">
          <Link to={"/login"}>Login </Link>
          to Comment
        </h2>
      )}
      <div>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant={"danger"} message={error} />
        ) : (
          comments.map((comment) => (
            <div className="comment line">
              <h3>{comment.author}</h3>
              <Rating
                value={comment.rate}
                text={
                  <LikeComment comment={comment} productId ={productId}  page={page} />
                }
              />
              <p>{comment.text}</p>
            </div>
          ))
        )}
      </div>

      <Pagination count={count} paginateBy={4} />
    </div>
  );
};

export default Comments;
