import { Link } from "react-router-dom";
import labelRegionDistribution from "../assets/label_region_distribution.png";

export default function Report() {
  return (
    <div className="min-h-screen px-6 md:px-12 lg:px-24 py-16 space-y-16">
      
      {/* HEADER */}
      <div className="text-center mb-12 animate-fade-in">
        <h1 className="text-4xl font-bold">Classification Report</h1>
        <p className="text-stone-400 max-w-2xl mx-auto mt-2">
          View regional distribution per cluster.
        </p>
      </div>

      {/* IMAGE */}
        <img 
          src={labelRegionDistribution} 
          alt="Label Region Distribution" 
          className="mx-auto mt-8 w-64 rounded-xl"
        />

      {/* RESULTS TABLE */}
      <section className="space-y-6">
        <div className="overflow-x-auto rounded-xl bg-stone-900/50">
          <table className="w-full text-left text-stone-300 text-sm">
            <thead className="bg-stone-900/80">
              <tr>
                <th className="px-4 py-3">Artifact ID</th>
                <th className="px-4 py-3">Predicted Region</th>
                <th className="px-4 py-3">Confidence</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-t border-stone-800/70">
                <td className="px-4 py-3">—</td>
                <td className="px-4 py-3">—</td>
                <td className="px-4 py-3">—</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
        
      {/* Back link */}
        <div className="text-center pt-4">
          <Link
            to="/"
            className="text-amber-400 hover:text-amber-300 transition underline text-lg"
          >
            ← Back to Home
          </Link>
        </div>
    </div>
  );
}
