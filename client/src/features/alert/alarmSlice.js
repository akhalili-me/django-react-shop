import { createSlice } from "@reduxjs/toolkit";
import { setAlertReducer, hideAlertReducer } from "./alarmReducers";

export const alarmSlice = createSlice({
  name: "alarm",
  initialState: { message: null, type: null, show: false },
  reducers: {
    setAlarm: setAlertReducer,
    hideAlarm: hideAlertReducer,
  },
});

export const { setAlarm, hideAlarm } = alarmSlice.actions;

export default alarmSlice.reducer;
