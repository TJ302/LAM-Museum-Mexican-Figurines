import React from "react";
import { Link } from "react-router-dom";

export default function About() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <h1 className="text-3xl font-bold mb-4">About This Project</h1>
      <p className="max-w-xl text-center">
        This page will describe how the Digit CSV Classifier works, its goals,
        and the model architecture used. You can explain the dataset, accuracy,
        and key learnings here.
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
