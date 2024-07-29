import React from "react";

import Header from "./components/Header";
import FormUploadImage from "./components/FormUploadImage";
import FormInput from "./components/FormInput";
import PreviewTable from "./components/PreviewTable";

export default function App() {
  return (
    <>
      <div className="container">
        <div className="row">
          <div className="col-12 col-md-5">
            <div className="row">
              <Header />
              <div className="col-12 mb-2">
                <FormUploadImage />
              </div>
              <div className="col-12 mb-2">
                <FormInput />
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
