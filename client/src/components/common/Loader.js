import React from 'react'
import Spinner from 'react-bootstrap/Spinner';

const Loader = () => {
  return (
		<Spinner animation="border" role="status" className='loader'>
			<span className="visually-hidden">Loading...</span>
		</Spinner>
  );
}

export default Loader