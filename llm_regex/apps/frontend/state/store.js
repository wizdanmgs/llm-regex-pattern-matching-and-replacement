import { configureStore } from "@reduxjs/toolkit";
import previewReducer from "./previewSlice";

export const store = configureStore({
  reducer: {
    preview: previewReducer,
  },
});
