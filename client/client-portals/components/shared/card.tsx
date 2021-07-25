import React from "react";
import Link from "next/link";
import { Button } from "@/shared/index";

const Card = ({ name, desc, url }) => {
  return (
    <div className="md:w-4/5 w-full px-8 py-8 mx-auto bg-white rounded-lg shadow-md mt-6">
      <div className="mt-2">
        <p className="text-2xl font-bold text-gray-700">{name}</p>
        <p className="mt-2 text-gray-600 w-6/7 overflow-auto no-scrollbar word-wrap">
          {desc}
        </p>
      </div>
      <Link href={url}>
        <Button btnStyle="primary">Open Contributors' Applications</Button>
      </Link>
    </div>
  );
};

export default Card;
