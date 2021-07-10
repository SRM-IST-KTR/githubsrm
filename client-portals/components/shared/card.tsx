import React from "react";
import Link from "next/link";

const Card = ({ name, desc, url }) => {
  return (
    <div className="max-w-2xl px-8 py-4 mx-auto bg-white rounded-lg shadow-md ">
      <div className="mt-2">
        <p className="text-2xl font-bold text-gray-700">{name}</p>
        <p className="mt-2 text-gray-600 ">{desc}</p>
      </div>
      <Link href={url}>
        <button className="flex rounded-xl font-bold items-center my-3  bg-base-teal p-3">
          Open
        </button>
      </Link>
    </div>
  );
};

export default Card;
