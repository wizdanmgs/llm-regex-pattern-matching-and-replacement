import { createSlice } from "@reduxjs/toolkit";

const previewSlice = createSlice({
  name: "preview",
  initialState: {
    records: [],
    loading: false,
  },
  reducers: {
    setPreviewRecords: (state, action) => {
      state.records = action.payload;
    },
    setPreviewLoading: (state, action) => {
      state.loading = action.payload;
    },
  },
});

export const { setPreviewRecords, setPreviewLoading } = previewSlice.actions;

export default previewSlice.reducer;
