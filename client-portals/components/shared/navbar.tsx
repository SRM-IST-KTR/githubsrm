import React, { useContext } from "react";
import Link from "next/link";
import { AuthContext } from "../../context/AuthContext";

const Navbar = ({ links }) => {
  const authContext = useContext(AuthContext);
  const User = authContext.user;

  return (
    <div className="flex flex-row justify-around text-white my-6">
      <h2 className="mt-5 mr-5 font-medium">Hi, {User.user}</h2>
      {links.map((item) => (
        <div className="mx-2 text-xl p-3  border-b-4 border-base-teal">
          <Link href={item.link}>{item.name}</Link>
        </div>
      ))}
      <button
        onClick={authContext.logoutHandler}
        className="bg-base-green p-2 mx-2 rounded text-xl"
      >
        Logout
      </button>
    </div>
  );
};

export default Navbar;
