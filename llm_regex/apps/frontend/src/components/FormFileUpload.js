import React, { useState } from "react";

import { useDispatch } from "react-redux";
import { setPreviewRecords, setPreviewLoading } from "../../state/previewSlice";

import { FilePond, registerPlugin } from "react-filepond";
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import "filepond/dist/filepond.min.css";

registerPlugin(FilePondPluginFileValidateType);

export default function FormFile() {
  const dispatch = useDispatch();

  const [files, setFiles] = useState([]);
  const [serverId, setServerId] = useState("");

  const fileValidateTypeLabelExpectedTypesMap = {
    "text/csv": "CSV",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
      "Excel",
    "application/vnd.ms-excel": "Excel",
  };
  const acceptedFileTypes = Object.keys(fileValidateTypeLabelExpectedTypesMap);
  const server = {
    process: "/api/file/",
    revert: `/api/file/${serverId}`,
  };

  const handleOnAddFile = (error, file) => {
    if (!error) {
      dispatch(setPreviewLoading(true));
    }
  };

  const handleOnRemoveFile = (error, _) => {
    if (!error) {
      dispatch(setPreviewRecords([]));
    }
  };

  const handleOnProcessFile = (error, file) => {
    if (!error) {
      const serverId = JSON.parse(file.serverId);
      setServerId(serverId.data.id);
      dispatch(setPreviewRecords(JSON.parse(serverId.table)));
      dispatch(setPreviewLoading(false));
    }
  };

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
                onprocessfile={(error, file) =>
                  handleOnProcessFile(error, file)
                }
                onaddfile={(error, file) => handleOnAddFile(error, file)}
                onremovefile={(error, file) => handleOnRemoveFile(error, file)}
                allowMultiple={false}
                server={server}
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
