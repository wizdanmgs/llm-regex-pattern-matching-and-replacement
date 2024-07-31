import React, { useState } from "react";
import Cookies from "js-cookie";
import { useSelector, useDispatch } from "react-redux";
import {
  setPreviewRecords,
  setPreviewLoading,
  setPreviewSameFile,
} from "../../state/previewSlice";

export default function FormNlp() {
  const dispatch = useDispatch();
  const [error, setError] = useState({ status: false, message: "" });
  const [loading, setLoading] = useState(false);

  const handleOnSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = JSON.stringify(Object.fromEntries(formData));

    dispatch(setPreviewLoading(true));
    setLoading(true);
    setError({ status: false, message: "" });

    fetch("/api/nlp/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
      body: data,
    })
      .then((response) => response.json())
      .then((response) => {
        if (response.status !== 200) {
          setError({
            status: true,
            message: response.message,
          });
        }
        setLoading(false);
        dispatch(setPreviewLoading(false));
        dispatch(setPreviewSameFile(true));
        dispatch(setPreviewRecords(JSON.parse(response.data.table)));
      })
      .catch((_) => {
        setError({
          status: true,
          message: "Sorry, we can't process your query. Try another?",
        });
        setLoading(false);
        dispatch(setPreviewLoading(false));
        dispatch(setPreviewSameFile(true));
      });
  };

  return (
    <div className="card py-2 h-100">
      <div className="card-body">
        <form onSubmit={handleOnSubmit}>
          <fieldset>
            <legend>2. Describe what data you want to replace</legend>
            <div>
              <textarea
                className={`form-control ${error.status ? "is-invalid" : ""}`}
                name="query"
                rows="5"
                required
                placeholder="e.g. Find email addresses in the Email column and replace them with 'REDACTED'."
              ></textarea>
              <div className={`${error.status ? "d-none" : ""}`}>
                <small className={`${loading ? "d-none" : ""}`}>
                  Tip! Don't forget to include the column name.
                </small>
                <small className={`${!loading ? "d-none" : ""}`}>
                  Processing your request...
                </small>
              </div>
              <div
                className={`invalid-feedback ${error.status ? "" : "d-none"}`}
              >
                {error.message}
              </div>
              <input
                type="hidden"
                name="same_file"
                value={useSelector((state) => state.preview.sameFile)}
              />
            </div>
            <button
              type="submit"
              className="btn btn-primary mt-3 w-100"
              disabled={loading}
            >
              <span
                className={`spinner-border spinner-border-sm me-1 ${
                  loading ? "" : "d-none"
                }`}
                aria-hidden="true"
              ></span>
              <span>
                Submit <i className="fas fa-share"></i>
              </span>
            </button>
          </fieldset>
        </form>
      </div>
    </div>
  );
}
