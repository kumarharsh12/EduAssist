"use client";
import React, { useState } from "react";

function HomePage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    dateTime: "",
    topic: "",
    otherInfo: "",
    audio: null,
    pdfs: [],
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData({
      ...formData,
      [name]: files ? (name === "pdfs" ? Array.from(files) : files[0]) : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formDataToSend = new FormData();
    for (const key in formData) {
      if (key === "pdfs") {
        formData[key].forEach((file, index) => {
          formDataToSend.append(`pdfs`, file);
        });
      } else {
        formDataToSend.append(key, formData[key]);
      }
    }

    try {
      const response = await fetch("http://localhost:8000/process/", {
        method: "POST",
        body: formDataToSend,
      });

      if (response.ok) {
        alert("Form submitted successfully!");
        setFormData({
          name: "",
          email: "",
          subject: "",
          dateTime: "",
          topic: "",
          otherInfo: "",
          audio: null,
          pdfs: [],
        }); // Reset form
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (err) {
      alert("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="max-w-lg mx-auto bg-gray-100 bg-opacity-5 p-6 rounded-lg shadow-md my-10">
      <h1 className="text-xl font-bold text-center text-white mb-4">
        Submit Your Details
      </h1>

      <form onSubmit={handleSubmit}>
        {/* Audio Upload */}
        <div className="mb-4">
          <label className="block text-gray-100">Upload Audio</label>
          <div className="bg-gray-100 bg-opacity-15 w-full h-64 mt-1 p-2 border-slate-700 rounded flex items-center justify-center relative">
            <input
              type="file"
              name="audio"
              accept="audio/*"
              onChange={handleChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              required
            />
            <button
              type="button"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
            >
              Choose File
            </button>
          </div>
        </div>
        {/* PDFs Upload */}
        <div className="mb-4">
          <label className="block text-gray-100">Upload PDFs</label>
          <div className="bg-gray-100 bg-opacity-15 w-full h-64 mt-1 p-2 border-slate-700 rounded flex items-center justify-center relative">
            <input
              type="file"
              name="pdfs"
              accept="application/pdf"
              onChange={handleChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              multiple
              required
            />
            <button
              type="button"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
            >
              Choose Files
            </button>
          </div>
        </div>

        {/* Form Fields */}
        {[
          { label: "Name", name: "name", type: "text" },
          { label: "Email", name: "email", type: "email" },
          { label: "Subject", name: "subject", type: "text" },
          { label: "Date & Time", name: "dateTime", type: "datetime-local" },
          { label: "Topic", name: "topic", type: "text" },
          { label: "Other Info", name: "otherInfo", type: "text" },
        ].map(({ label, name, type }) => (
          <div className="mb-4" key={name}>
            <label className="block text-gray-100">{label}</label>
            <input
              type={type}
              name={name}
              value={formData[name]}
              onChange={handleChange}
              className="w-full mt-1 p-2 border-slate-700 rounded bg-gray-100 bg-opacity-15"
              required
            />
          </div>
        ))}

        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 w-full mt-4"
        >
          Submit
        </button>
      </form>
    </div>
  );
}

export default HomePage;
