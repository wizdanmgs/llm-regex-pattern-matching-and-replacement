import { createSlice } from "@reduxjs/toolkit";

const nlpSlice = createSlice({
  name: "nlp",
  initialState: {
    error: {
      status: false,
      message: "Sorry, we can't understand your query. Try another?",
    },
  },
  reducers: {
    setNlpError: (state, action) => {
      state.error = action.payload;
    },
  },
});

export const { setNlpError } = nlpSlice.actions;

export default nlpSlice.reducer;
