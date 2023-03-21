import { useEffect,useState,useCallback } from 'react';
import Rating from '../common/Rating'
import {isAuthenticated} from '../../utility/auth'
import CommentForm from './CommentForm';
import { fetchProductComments } from '../../utility/comment';
import { Link } from 'react-router-dom';


const Reviews = ({productId}) => {
    const [comments, setComments] = useState([]);

    const getComments = useCallback(async () => {
        const response = await fetchProductComments(productId);
        setComments(response.data);
    }, [productId]);
      
    
    useEffect(() => {
        getComments();
    }, [getComments]);


    return (
        <>
            {isAuthenticated() ? <CommentForm productId={productId} getComments={getComments} /> :(
                <h2 className='bold mb-4'>
                    <Link to={'/login'}>Login </Link>
                    to Comment
                </h2>
            )}
            <div>
                {comments.map((c) =>
                    <div className='comment line'>
                        <h3>{c.author}</h3>
                        <Rating value={c.rate}/>
                        <p>{c.text}</p>
                    </div>
                )}
            </div>
        </>
    )
}

export default Reviews;
