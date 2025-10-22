import React from "react";
import { Link } from "react-router-dom";

export default function Contact() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <h1 className="text-3xl font-bold mb-4">Contact Us</h1>
      <p className="max-w-xl text-center mb-4">
        Include your project team’s contact information or a contact form here.
        For example, name, email, and GitHub links.
      </p>
      <Link
        to="/"
        className="mt-6 text-emerald-500 hover:text-emerald-400 underline"
      >
        ← Back to Home
      </Link>
    </div>
  );
}
