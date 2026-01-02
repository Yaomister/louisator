import { ChangeEvent, FormEvent, useState } from "react";

import "../stylesheets/AddKnownFacesForm.css";

export const AddKnownFacesForm = ({ close }: { close: () => void }) => {
  const [image, setImage] = useState<File | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    console.error(image);
    e.preventDefault();
  };

  return (
    <div className="add-known-faces-form">
      <div className="top-bar">
        <h4 className="form-title">Add people you know!</h4>
        <button className="close" onClick={close}>
          x
        </button>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="image">Upload image</label>
          <input
            id="image"
            type="file"
            accept="image/*"
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              const file = e.target.files?.[0] ?? null;
              setImage(file);
            }}
          />
        </div>
        <div className="field">
          <label htmlFor="name">Name</label>
          <input type="text" id={"name"}></input>
        </div>
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
    </div>
  );
};
