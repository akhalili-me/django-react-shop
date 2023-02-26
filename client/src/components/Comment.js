import Rating from './Rating'

const Comment = ({comments}) => {
    if (!comments) {
        return (
        <div>
            No Comments Yet
        </div> 

        )
    }    
    return (
        <div>
            {comments.map((c) =>
                <div className='comment line'>
                    <h3>{c.author}</h3>
                    <Rating value={c.rate}/>
                    <p>{c.text}</p>
                </div>
            )}
        </div>
    )
}

export default Comment;
