import React from "react";

export default function FormInput() {
  return (
    <div className="card mb-2">
      <div className="card-body">
        <form>
          <fieldset>
            <legend>2. Describe what data you want to replace</legend>
            <div>
              <textarea
                className="form-control"
                id="exampleTextarea"
                rows="3"
                placeholder="e.g. Find email addresses in the Email column and replace them with 'REDACTED'."
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary mt-2 w-100">
              Submit
            </button>
          </fieldset>
        </form>
      </div>
    </div>
  );
}
