import React from "react";

import { useSelector } from "react-redux";

import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";

export default function PreviewTable() {
  const records = useSelector((state) => state.preview.records);
  const loading = useSelector((state) => state.preview.loading);

  const column =
    records.length > 0 &&
    Object.keys(records[0]).map((head) => {
      return {
        field: head,
      };
    });

  const pagination = true;
  const paginationPageSize = 10;
  const paginationPageSizeSelector = false;

  return (
    <div className="card py-2 h-100">
      <div className="card-body">
        <legend>Preview</legend>
        <div className="ag-theme-quartz" style={{ height: "563px" }}>
          <AgGridReact
            rowData={records}
            columnDefs={column}
            pagination={pagination}
            paginationPageSize={paginationPageSize}
            paginationPageSizeSelector={paginationPageSizeSelector}
            loading={loading}
          />
        </div>
        <div className="mt-3">
          {/* <button
            className="btn btn-secondary float-start"
            style={{ width: "49.2%" }}
          >
            <i className="fas fa-chevron-left"></i> Back
          </button>
          <button
            className="btn btn-success float-end"
            style={{ width: "49.2%" }}
          >
            <i className="fas fa-arrow-down"></i> Download
          </button> */}
          <button className="btn btn-success float-end w-100">
            Download Result <i className="fas fa-download"></i>
          </button>
        </div>
      </div>
    </div>
  );
}
