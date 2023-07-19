import React from "react";
import Form from "react-bootstrap/Form";

const AddressItem = ({ address, selectedAddressId, onChangeAddress }) => {
  const fullAddress = `${address.state}, ${address.city} ${address.street_address}. 
    <strong>Pelak:</strong> ${address.house_number},
    <strong>Postal Code:</strong> ${address.postal_code}`;

  return (
    <Form.Check
      name="address"
      checked={selectedAddressId === address.id}
      type="radio"
      value={address.id}
      label={<span dangerouslySetInnerHTML={{ __html: fullAddress }} />}
      onChange={onChangeAddress}
    />
  );
};

export default AddressItem;
