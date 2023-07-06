import storage from "redux-persist/lib/storage";
import { persistReducer } from "redux-persist";
import rootReducer from "./rootReducer";

const persistConfig = {
  key: "root",
  storage,
  blacklist: ["productList","auth"],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export default persistedReducer;
