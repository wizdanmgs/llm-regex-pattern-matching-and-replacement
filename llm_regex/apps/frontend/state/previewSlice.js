import { createSlice } from "@reduxjs/toolkit";

const previewSlice = createSlice({
  name: "preview",
  initialState: {
    records: [],
    loading: false,
    sameFile: false,
  },
  reducers: {
    setPreviewRecords: (state, action) => {
      state.records = action.payload;
    },
    setPreviewLoading: (state, action) => {
      state.loading = action.payload;
    },

    setPreviewSameFile: (state, action) => {
      state.sameFile = action.payload;
    },
  },
});

export const { setPreviewRecords, setPreviewLoading, setPreviewSameFile } =
  previewSlice.actions;

export default previewSlice.reducer;
