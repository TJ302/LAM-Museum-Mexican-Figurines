import React, { useEffect, useState } from "react";

export default function Report() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [rows, setRows] = useState([]);
  const [probabilities, setProbabilities] = useState({});
  const [pngUrl, setPngUrl] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  useEffect(() => {
    async function fetchResults() {
      try {
        const res = await fetch("http://127.0.0.1:5000/api/cluster-results");
        if (!res.ok) throw new Error("Failed to load clustering results");
        const data = await res.json();
        if (!data.success) throw new Error(data.error || "Unknown error");

        setRows(data.rows || []);
        setProbabilities(data.probabilities || {});
        setPngUrl(
          "http://127.0.0.1:5000" +
            (data.pngUrl || "/static/label_region_distribution.png")
        );
        setDownloadUrl(
          "http://127.0.0.1:5000" + (data.downloadUrl || "/download/clusters")
        );
      } catch (err) {
        console.error(err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchResults();
  }, []);

  return (
    <div className="min-h-screen px-6 md:px-12 lg:px-24 py-16 space-y-16">
      {/* HEADER */}
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl font-bold">Clustering Report</h1>
        <p className="text-stone-400 max-w-2xl mx-auto mt-2">
          Region distributions from KMeans clustering on WFU feature vectors.
        </p>
      </div>

      {/* STATUS */}
      {loading && (
        <p className="text-center text-stone-400">Loading clustering results…</p>
      )}
      {error && (
        <p className="text-center text-red-400">
          Could not load results: {error}
        </p>
      )}

      {!loading && !error && (
        <>
          {/* PNG / "venn" diagram */}
          <section className="space-y-4">
            <h2 className="text-2xl font-semibold text-center">
              Region Distribution Visualization
            </h2>
            <div className="flex justify-center">
              <div className="max-w-xl w-full rounded-2xl overflow-hidden bg-stone-900 border border-stone-800">
                <img
                  src={pngUrl}
                  alt="Cluster region distribution"
                  className="w-full h-auto"
                />
              </div>
            </div>
          </section>

          {/* DOWNLOAD BUTTON */}
          <section className="text-center space-y-4">
            <h2 className="text-xl font-semibold">
              Download Full Clustering Results
            </h2>
            <p className="text-stone-400 max-w-xl mx-auto">
              Download a text file containing each image ID, its labeled region,
              and its assigned cluster along with per-cluster region
              probabilities.
            </p>
            <a
              href={downloadUrl}
              className="inline-flex items-center px-5 py-2 rounded-lg bg-amber-500 text-stone-900 font-semibold shadow hover:scale-105 transition transform"
            >
              Download clustering_results.txt
            </a>
          </section>

          {/* PROBABILITY TABLE */}
          <section className="space-y-6">
            <h2 className="text-2xl font-semibold text-center">
              Region Probabilities by Cluster
            </h2>
            <div className="overflow-x-auto rounded-xl bg-stone-900/50">
              <table className="w-full text-left text-stone-300 text-sm">
                <thead className="bg-stone-900/80">
                  <tr>
                    <th className="px-4 py-3">Cluster</th>
                    <th className="px-4 py-3">Region</th>
                    <th className="px-4 py-3">Count</th>
                    <th className="px-4 py-3">Probability</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(probabilities).map(([clusterId, regions]) =>
                    Object.entries(regions).map(
                      ([regionName, { count, probability }]) => (
                        <tr
                          key={`${clusterId}-${regionName}`}
                          className="border-t border-stone-800/70"
                        >
                          <td className="px-4 py-3">{clusterId}</td>
                          <td className="px-4 py-3">{regionName}</td>
                          <td className="px-4 py-3">{count}</td>
                          <td className="px-4 py-3">
                            {(probability * 100).toFixed(1)}%
                          </td>
                        </tr>
                      )
                    )
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
