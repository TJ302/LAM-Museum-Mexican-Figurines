import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="flex justify-center space-x-4 bg-neutral-900 py-4 shadow-lg">
      <Link
        to="/"
        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-xl"
      >
        Home
      </Link>
      <Link
        to="/about"
        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-xl"
      >
        About
      </Link>
      <Link
        to="/regional"
        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-xl"
      >
        Regional Info
      </Link>
      <Link
        to="/contact"
        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-xl"
      >
        Contact Us
      </Link>
    </nav>
  );
}
