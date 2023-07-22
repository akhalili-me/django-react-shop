import { createAsyncThunk } from "@reduxjs/toolkit";
import authAxios from "../../utility/api";
import { setAlarm } from "../alert/alarmSlice";

const currentTimestamp = Date.now();
const currentDateString = new Date(currentTimestamp).toISOString();

export const paymentSuccessfull = createAsyncThunk(
  "paymentOperations/paymentSuccessfull",
  async ({ paymentId }) => {
    try {
      await authAxios.patch(`/cart/payment/${paymentId}`, {
        status: "paid",
        paid_at: currentDateString,
      });
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      throw new Error(errorMessage);
    }
  }
);

export const paymentFailed = createAsyncThunk(
  "paymentOperations/paymentSuccessfull",
  async ({ paymentId }, { dispatch }) => {
    try {
      await authAxios.patch(`/cart/payment/${paymentId}`, {
        status: "failed",
      });
      dispatch(
        setAlarm({
          message: "Payment failed to submit.",
          type: "danger",
        })
      );
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message;
      dispatch(setAlarm({ message: errorMessage, type: "danger" }));
      throw new Error(errorMessage);
    }
  }
);
