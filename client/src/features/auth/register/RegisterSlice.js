import { createSlice } from "@reduxjs/toolkit";
import { clearRegisterErrorsReducers, register } from "./RegisterReducers";

export const registerSlice = createSlice({
	name: "login",
	initialState: {
		loading: null,
		error: null,
		success: null,
	},
	reducers: { 
		clearRegisterErrors: clearRegisterErrorsReducers
	},
	extraReducers: (builder) => {
		builder

			// Register
			.addCase(register.pending, (state) => {
				state.loading = true;
			})
			.addCase(register.fulfilled, (state, action) => {
				state.loading = false;
				state.success = true;
			})
			.addCase(register.rejected, (state, action) => {
				state.loading = false;
				state.error = action.error.message;
			})
	},
});

export const { clearRegisterErrors } = registerSlice.actions;
export default registerSlice.reducer;
