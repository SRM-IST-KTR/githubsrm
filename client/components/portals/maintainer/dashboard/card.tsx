import React from "react";

const card = () => {
  return (
    <div className="max-w-2xl px-8 py-4 mx-auto bg-white rounded-lg shadow-md ">
      <div className="mt-2">
        <p className="text-2xl font-bold text-gray-700">Project 1</p>
        <p className="mt-2 text-gray-600 ">
          Lorem ipsum dolor sit, amet consectetur adipisicing elit. Tempora
          expedita dicta totam aspernatur doloremque. Excepturi iste iusto eos
        </p>
      </div>

      <button className="flex rounded-xl font-bold items-center my-3  bg-base-teal p-3">
        Open
      </button>
    </div>
  );
};

export default card;
