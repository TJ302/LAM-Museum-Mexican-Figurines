import React from "react";
import { Link } from "react-router-dom";

export default function Regional() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh]">
      <h1 className="text-3xl font-bold mb-4">Regional Information</h1>
      <p className="max-w-xl text-center">
        This section can include visualizations or regional performance metrics
        for your model. For instance, how accuracy differs across datasets.
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
