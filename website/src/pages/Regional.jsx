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

      {/* Colima */}
      <div className="max-w-2xl mb-8 p-6 border rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-2">Colima</h2>
        <p className="italic mb-2">Western Mexico (c. 300 BCE – 300 CE)</p>
        <p className="mb-2">
          The Colima culture thrived in Western Mexico. Well-known for its lifelike ceramic figurines, 
          the Colima specialized in depicting animals, humans, and scenes from everyday life. 
          Artifacts were often placed in tombs to aid the deceased in the afterlife. 
          Colima figurines are distinguishable by their simple features and minimal adornments.
        </p>
        <h3 className="font-semibold mb-1">Characteristics</h3>
        <p>
          Colima figurines were typically hand-crafted. The eyes of these figurines are usually slits or lines in the clay 
          of the figurine’s face. Sometimes, the eyes are large circles. Noses are either in small, rounded “O” shape or a triangle shape. 
          The mouths of Colima figurines are small and often have simple smiles. Their adornments are minimal.
        </p>
      </div>

      {/* Nayarit */}
      <div className="max-w-2xl mb-8 p-6 border rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-2">Nayarit</h2>
        <p className="italic mb-2">Western Mexico (c. 200 BCE – 300 CE)</p>
        <p className="mb-2">
          The Nayarit culture was found alongside the pacific coast of Western Mexico. 
          Their figurines are extravagant, boasting many accessories, for which they are recognizable. 
          Figurines also reflect communal life and social rituals, showing a deep connection to the spiritual and social worlds.
        </p>
        <h3 className="font-semibold mb-1">Characteristics</h3>
        <p>
          Nayarit figurines were created using a mix of hand-crafted and molded techniques. 
          The eyes of figurines are generally in an almond or slit shape, while the nose is straight or hooked. 
          Nayarit figurine mouths are generally small with neutral expressions. 
          They often have numerous adornments, like large earrings or plug styles, necklaces, and headdresses. 
          Sometimes they have hats or headgear.
        </p>
      </div>

      {/* Chipicuaro */}
      <div className="max-w-2xl mb-8 p-6 border rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-2">Chipicuaro</h2>
        <p className="italic mb-2">Northwest Central Mexico (c. 500 BCE – 300 CE)</p>
        <p className="mb-2">
          The Chupicuaro culture is one of Mesoamerica’s earliest ceramic traditions, originating in the Bajio region of central Mexico. 
          They are typically found in burial places and hold ritual significance. 
          The figurines’ distinctive appearances are marked by highly stylized human forms and detailed adornments.
        </p>
        <h3 className="font-semibold mb-1">Characteristics</h3>
        <p>
          Chipicuaro figurines were typically hand-carded using clay. 
          The figurine’s eyes are usually small slits or dot-shaped impressions, often with minimal detailing. 
          Their noses are small, simple, and often triangular or left undefined, while Chipicuaro figurine mouths are small and usually closed or downturned. 
          The adornments these figurines have may include earrings, necklaces, and detailed hairstyles or headdresses.
        </p>
      </div>
      
      <Link
        to="/"
        className="mt-6 text-emerald-500 hover:text-emerald-400 underline"
      >
        ← Back to Home
      </Link>
    </div>
  );
}
