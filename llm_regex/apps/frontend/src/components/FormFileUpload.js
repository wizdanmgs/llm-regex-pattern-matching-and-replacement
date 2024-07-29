import React, { useState } from "react";
import { FilePond, registerPlugin } from "react-filepond";
import FilePondPluginImageExifOrientation from "filepond-plugin-image-exif-orientation";
import FilePondPluginImagePreview from "filepond-plugin-image-preview";
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import "filepond/dist/filepond.min.css";
import "filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css";

registerPlugin(
  FilePondPluginImageExifOrientation,
  FilePondPluginImagePreview,
  FilePondPluginFileValidateType
);

export default function FormFile() {
  const [files, setFiles] = useState([]);
  const fileValidateTypeLabelExpectedTypesMap = {
    "text/csv": "CSV",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
      "Excel",
    "application/vnd.ms-excel": "Excel",
  };
  const acceptedFileTypes = Object.keys(fileValidateTypeLabelExpectedTypesMap);

  return (
    <div className="card py-2 h-100">
      <div className="card-body">
        <form>
          <fieldset>
            <legend>1. Upload your file</legend>
            <div className="mt-4">
              <FilePond
                files={files}
                onupdatefiles={setFiles}
                allowMultiple={false}
                server="/api/file/"
                name="file"
                labelIdle='Drag & Drop your file or <span class="filepond--label-action">Browse</span>'
                acceptedFileTypes={acceptedFileTypes}
                fileValidateTypeLabelExpectedTypesMap={
                  fileValidateTypeLabelExpectedTypesMap
                }
              />
              <small id="imageHelp" className="form-text text-muted">
                Allowed file types: .csv, .xls, .xlsx
              </small>
            </div>
          </fieldset>
        </form>
      </div>
    </div>
  );
}
