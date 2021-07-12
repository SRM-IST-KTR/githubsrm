import React, { useContext } from "react";
import Link from "next/link";
import { AuthContext } from "../../../../context/authContext";

const Adminnavbar = () => {
  const authContext = useContext(AuthContext);

  return (
    <div className="flex flex-row justify-center text-white my-6">
      <div className="mx-2 text-xl p-3  border-b-4 border-base-teal">
        <Link href="/admin/dashboard">Project Applications</Link>
      </div>
      <div className="mx-2 text-xl p-3 border-b-4 border-base-teal">
        <Link href="/admin/dashboard/accepted-projects">Accepted Projects</Link>
      </div>
      <button
        onClick={authContext.logoutHandler}
        className="bg-base-green p-2 mx-2 rounded text-xl"
      >
        Logout
      </button>
    </div>
  );
};

export default Adminnavbar;
