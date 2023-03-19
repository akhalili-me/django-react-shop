
export const setAlertReducer = (state, action) => {
    state.message = action.payload.message;
    state.type = action.payload.type
    state.show = true
};


export const hideAlertReducer = (state,action) => {
    state.message = ''
    state.type = ''
    state.show = false
}