import React from "react";

export default function FormInput() {
  return (
    <div className="card py-2 h-100">
      <div className="card-body">
        <form>
          <fieldset>
            <legend>2. Describe what data you want to replace</legend>
            <div>
              <textarea
                className="form-control"
                id="exampleTextarea"
                rows="6"
                placeholder="e.g. Find email addresses in the Email column and replace them with 'REDACTED'."
              ></textarea>
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
