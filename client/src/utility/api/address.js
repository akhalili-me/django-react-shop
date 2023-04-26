import authAxios from "../api";

export const fetchUserAddresses = async () => {
  const response = await authAxios.get(`/accounts/address`);
  return response;
};

export const addAddress = async (address) => {
  const { state, city, phone, postalCode, streetAddress, houseNumber } =
    address;
  await authAxios.post(`/accounts/address/`, {
    state: state,
    city: city,
    phone: phone,
    postal_code: postalCode,
    street_address: streetAddress,
    house_number: houseNumber,
  });
};

export const fetchAddressById = async (addressId) => {
  const response = await authAxios.get(`/accounts/address/${addressId}`);
  return response;
};
