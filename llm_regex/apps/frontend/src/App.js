import React from "react";

import Title from "./components/Title";
import FormFileUpload from "./components/FormFileUpload";
import FormNlp from "./components/FormNlp";
import PreviewTable from "./components/PreviewTable";

export default function App() {
  return (
    <>
      <div className="container">
        <div className="row">
          <div className="col-12 col-md-5">
            <div className="row">
              <Title />
              <div className="col-12 mb-2">
                <FormFileUpload />
              </div>
              <div className="col-12 mb-2">
                <FormNlp />
              </div>
            </div>
          </div>
          <div className="col-12 col-md-7 mb-4">
            <PreviewTable />
          </div>
        </div>
      </div>
    </>
  );
}
