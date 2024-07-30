import React, { useState } from "react";
import Cookies from "js-cookie";
import { useDispatch } from "react-redux";
import { setPreviewRecords, setPreviewLoading } from "../../state/previewSlice";

export default function FormNlp() {
  const dispatch = useDispatch();
  const [error, setError] = useState({ status: false, message: "" });

  const handleOnSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = JSON.stringify(Object.fromEntries(formData));

    dispatch(setPreviewLoading(true));
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

        dispatch(setPreviewLoading(false));
      })
      .catch((_) => {
        dispatch(setPreviewLoading(false));
        setError({
          status: true,
          message: "Sorry, we can't process your query. Try another?",
        });
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
                <small>Tip! Don't forget to include the column name.</small>
              </div>
              <div
                className={`invalid-feedback ${error.status ? "" : "d-none"}`}
              >
                {error.message}
              </div>
            </div>
            <button type="submit" className="btn btn-primary mt-3 w-100">
              Submit <i className="fas fa-share"></i>
            </button>
          </fieldset>
        </form>
      </div>
    </div>
  );
}
