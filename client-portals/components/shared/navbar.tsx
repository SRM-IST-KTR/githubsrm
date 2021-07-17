import React, { useContext, useEffect, useState } from "react";
import Link from "next/link";
import { AuthContext } from "../../context/authContext";
import LogoutIcon from "../../utils/icons/logout";

const Navbar = ({ links }) => {
  const authContext = useContext(AuthContext);

  return (
    <div className="flex flex-row justify-around text-white py-3 bg-base-black">
      <h2 className="mt-5 mr-5 font-medium">Hi, {authContext.username}</h2>
      {links.map((item) => (
        <div
          key={item.name}
          className="mx-2 text-xl p-3 border-b-4 border-base-teal hover:border-base-green transform hover:scale-105 hover:translate--y"
        >
          <Link href={item.link}>{item.name}</Link>
        </div>
      ))}
      <button
        onClick={authContext.logoutHandler}
        className="bg-base-green p-2 mx-2 rounded text-xl"
      >
        <div className="flex ">
          <span className="flex items-center">
            <LogoutIcon />
          </span>{" "}
          <span className="mx-1">Logout</span>
        </div>
      </button>
    </div>
  );
};

export default Navbar;
