import { configureStore } from "@reduxjs/toolkit";
import fileReducer from "./fileSlice";
import previewReducer from "./previewSlice";

export const store = configureStore({
  reducer: {
    file: fileReducer,
    preview: previewReducer,
  },
});
