import { configureStore } from "@reduxjs/toolkit";
import fileReducer from "./fileSlice";
import nlpReducer from "./nlpSlice";
import previewReducer from "./previewSlice";

export const store = configureStore({
  reducer: {
    file: fileReducer,
    nlp: nlpReducer,
    preview: previewReducer,
  },
});
