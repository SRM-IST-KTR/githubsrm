import React from "react";
import Card from "./card";

const index = () => {
  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <h2 className="text-4xl font-extrabold text-white mb-10">
        Hi, maintainer{" "}
      </h2>
      <div className="grid grid-cols-3 gap-4 ">
        {[1, 2, 3, 4, 5, 6, 7, 8].map(() => (
          <Card />
        ))}
      </div>
    </div>
  );
};

export default index;
