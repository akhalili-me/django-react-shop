import storage from "redux-persist/lib/storage";
import { persistReducer } from "redux-persist";
import rootReducer from "./rootReducer";

const persistConfig = {
  key: "root",
  storage,
  blacklist: ["product"],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export default persistedReducer;
