import React from "react";

import Header from "./components/Header";
import FormUploadImage from "./components/FormUploadImage";
import FormInput from "./components/FormInput";
import PreviewTable from "./components/PreviewTable";

export default function App() {
  return (
    <>
      <Header />
      <div className="main">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-5">
              <FormUploadImage />
              <FormInput />
            </div>
            <div className="col-md-7">
              <PreviewTable />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
