import { ChangeEvent, FormEvent, useState } from "react";

import "../stylesheets/AddKnownFacesForm.css";
import axios from "axios";
import { toast } from "react-hot-toast";

export const AddKnownFacesForm = ({ close }: { close: () => void }) => {
  const [image, setImage] = useState<File | null>(null);
  const [name, setName] = useState<string>("");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!image) return;
    const data = new FormData();
    data.append("file", image);
    data.append("name", name);
    try {
      const { status } = await axios.post(
        "http://localhost:8000/known-faces",
        data
      );

      console.error(status);
      if (status == 200) {
        toast.success("Image uploaded successfully!");
        close();
      }
    } catch (e) {
      console.error(e);
      toast.error("Could not upload image!");
    }
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
          <input
            type="text"
            id={"name"}
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              setName(e.target.value);
            }}
          ></input>
        </div>
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
    </div>
  );
};
