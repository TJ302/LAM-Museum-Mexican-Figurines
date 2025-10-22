import React from "react";
import DigitCsvClassifier from "../DigitCsvClassifier";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-10">
      <h1 className="text-3xl font-bold mb-4">Digit CSV Classifier</h1>
      <DigitCsvClassifier />
    </div>
  );
}
