import storage from "redux-persist/lib/storage";
import { persistReducer } from "redux-persist";
import rootReducer from "./rootReducer";

const persistConfig = {
  key: "root",
  storage,
  blacklist: ["loading"], // don't persist the 'loading' slice of state
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export default persistedReducer;
