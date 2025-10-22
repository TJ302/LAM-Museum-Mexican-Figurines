import React, { useState } from "react";
import * as tf from "@tensorflow/tfjs";
import Papa from "papaparse";

export default function DigitCsvClassifier() {
  const [status, setStatus] = useState("Upload a test CSV file to begin.");
  const [results, setResults] = useState(null);
  const [model, setModel] = useState(null);

  // ---- Load TF.js model (once) ----
  async function loadModel() {
    if (model) return model; // already loaded
  
    setStatus("Loading model...");
    try {
      const m = await tf.loadLayersModel("/tfjs_model/model.json");
      setModel(m);
      setStatus("✅ Model loaded. Ready to evaluate.");
      return m; // return the loaded model directly
    } catch (e) {
      console.error(e);
      setStatus(`❌ Error loading model: ${e.message}`);
      return null;
    }
  }
  
  // ---- Convert a CSV row into a flat 28x28 image array ----
  function rowToImage(row) {
    const pixels = [];
    for (let r = 1; r <= 28; r++) {
      for (let c = 1; c <= 28; c++) {
        const key = `${r}x${c}`;
        let val = row[key];
  
        // Handle missing or string values
        if (val === "" || val == null) val = 0;
        val = Number(val);
        if (isNaN(val)) val = 0;
  
        pixels.push(val / 255.0); // normalize 0–1
      }
    }
    return pixels;
  }
  

  // ---- Handle CSV upload ----
  async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    const m = await loadModel();  // get the actual model back
    if (!m) return;               // stop if failed
  
    setStatus(`Parsing ${file.name}...`);
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      complete: async (res) => {
        const data = res.data.slice(0, 10);
        setStatus(`Parsed ${data.length} rows. Running predictions...`);
  
        const images = data.map(rowToImage);
  
        console.log("First row:", data[0]);
        console.log("First image length:", images[0]?.length);
        console.log("First 20 pixels:", images[0]?.slice(0, 20));
  
        const xs = tf.tensor4d(
          new Float32Array(images.flat()),
          [images.length, 28, 28, 1]
        );
  
        try {
          const preds = m.predict(xs); // ✅ use the returned model
          const predLabels = Array.from(preds.argMax(-1).dataSync());
  
          const output = data.map((row, i) => ({
            ...row,
            prediction: predLabels[i],
          }));
  
          setResults(output);
          setStatus(`✅ Done. ${output.length} predictions ready.`);
        } catch (err) {
          console.error(err);
          setStatus(`❌ Prediction error: ${err.message}`);
        } finally {
          tf.dispose(xs);
        }
      },
    });
  }
  

  // ---- Download results as CSV ----
  function handleDownload() {
    if (!results) return;
    const csv = Papa.unparse(results);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "predictions.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  // ---- Render UI ----
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 flex flex-col items-center justify-center p-6">
      <h1 className="text-2xl font-bold mb-4">Digit CSV Classifier</h1>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileUpload}
        className="mb-4"
      />

      <p className="mb-4">{status}</p>

      {results && (
        <button
          onClick={handleDownload}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-xl"
        >
          Download predictions.csv
        </button>
      )}
    </div>
  );
}
