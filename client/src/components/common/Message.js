import React from 'react'
import Alert from 'react-bootstrap/Alert';

const Message = ({variant, message}) => {
  return (
		<Alert key={variant} variant={variant}>
			{message}
		</Alert>
  );
}

export default Message