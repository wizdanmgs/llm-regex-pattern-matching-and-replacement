import { createSlice } from "@reduxjs/toolkit";

const fileSlice = createSlice({
  name: "file",
  initialState: {
    id: "",
  },
  reducers: {
    setFileId: (state, action) => {
      state.id = action.payload;
    },
  },
});

export const { setFileId } = fileSlice.actions;

export default fileSlice.reducer;
