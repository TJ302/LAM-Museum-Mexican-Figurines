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

        {/* IMAGE */}
        <img 
          src={labelRegionDistribution} 
          alt="Label region distribution" 
          className="mx-auto mt-8 w-64 rounded-xl"
        />
      </div>
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
