import authAxios from "../api";

export const fetchUserAddresses = async () => {
  const response = await authAxios.get(`/accounts/address`);
  return response;
};

export const fetchAddressById = async (addressId) => {
  const response = await authAxios.get(`/accounts/address/${addressId}`);
  return response;
};

export const addAddress = async (address) => {
  const { state, city, phone, postal_code, street_address, house_number } =
    address;

  await authAxios.post(`/accounts/address/`, {
    state: state,
    city: city,
    phone: phone,
    postal_code: postal_code,
    street_address: street_address,
    house_number: house_number,
  });
};

export const updateAddress = async (address) => {
  const { id, state, city, phone, postal_code, street_address, house_number } =
    address;
    
  await authAxios.put(`/accounts/address/${id}/`, {
    id: 5,
    state: state,
    city: city,
    phone: phone,
    postal_code: postal_code,
    street_address: street_address,
    house_number: house_number,
  });
};

export const deleteAddress = async (addressId) => {
  await authAxios.delete(`/accounts/address/${addressId}`);
};
