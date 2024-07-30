import React from "react";

import { useDispatch, useSelector } from "react-redux";

export default function FormNlp() {
  const error = useSelector((state) => state.nlp.error);

  return (
    <div className="card py-2 h-100">
      <div className="card-body">
        <form>
          <fieldset>
            <legend>2. Describe what data you want to replace</legend>
            <div>
              <textarea
                className={`form-control ${error.status ? "is-invalid" : ""}`}
                id="exampleTextarea"
                rows="5"
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
