import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../../utility/api";

export const addAddress = createAsyncThunk(
	"addressOperations/addAddress",
	async ({state, city, phone, postal_code, street_address, house_number}) => {
		try {
          await authAxios.post(`/accounts/address/`, {
            state: state,
            city: city,
            phone: phone,
            postal_code: postal_code,
            street_address: street_address,
            house_number: house_number,
          });
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);
export const updateAddress = createAsyncThunk(
	"addressOperations/updateAddress",
	async ({ id, state, city, phone, postal_code, street_address, house_number }) => {
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
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);

export const deleteAddress = createAsyncThunk(
	"commentOperations/addComment",
	async (addressId) => {
		try {
			await authAxios.delete(`/accounts/address/${addressId}`);
		} catch (error) {
			const errorMessage =
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message;
			throw new Error(errorMessage);
		}
	}
);