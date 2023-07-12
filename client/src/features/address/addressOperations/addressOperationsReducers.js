import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";
import { setAlarm } from "../../alert/alarmSlice";
import { getUserAddresses } from "../addressList/addressListReducers";

export const addAddress = createAsyncThunk(
  "addressOperations/addAddress",
  async (
    { state, city, phone, postal_code, street_address, house_number },
    { dispatch }
  ) => {
    try {
      await authAxios.post(`/accounts/address/`, {
        state: state,
        city: city,
        phone: phone,
        postal_code: postal_code,
        street_address: street_address,
        house_number: house_number,
      });
      dispatch(
        setAlarm({ message: "Address added successfully.", type: "success" })
      );
      dispatch(getUserAddresses());
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);
export const updateAddress = createAsyncThunk(
  "addressOperations/updateAddress",
  async (
    { id, state, city, phone, postal_code, street_address, house_number },
    { dispatch }
  ) => {
    try {
      await authAxios.put(`/accounts/address/${id}/`, {
        id: 5,
        state: state,
        city: city,
        phone: phone,
        postal_code: postal_code,
        street_address: street_address,
        house_number: house_number,
      });

      dispatch(
        setAlarm({ message: "Address updated successfully.", type: "success" })
      );
      dispatch(getUserAddresses());
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);

export const deleteAddress = createAsyncThunk(
  "commentOperations/addComment",
  async (addressId, { dispatch }) => {
    try {
      await authAxios.delete(`/accounts/address/${addressId}`);
      dispatch(
        setAlarm({ message: "Address deleted successfully.", type: "success" })
      );
      dispatch(getUserAddresses());
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);
