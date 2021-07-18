import React from "react";
import Link from "next/link";
import { AuthContext } from "../context/authContext";
import Router from "next/router";

const IndexPage = () => {
  const authContext = React.useContext(AuthContext);

  React.useEffect(() => {
    if (authContext.isAuth) {
      if (authContext.isAdmin) {
        Router.push("/admin/dashboard");
      } else {
        Router.push("/maintainer/dashboard");
      }
    }
  }, [authContext]);

  return (
    <div className="min-h-screen bg-base-blue flex flex-col justify-center items-center">
      <Link href="/maintainer">
        <span className="py-7 cursor-pointer px-16 rounded-xl shadow-xl bg-base-green font-bold text-white transform hover:scale-110 hover:opacity-80">
          {" "}
          Maintainer
        </span>
      </Link>
      <Link href="/admin">
        <span className="py-7 cursor-pointer px-20 mt-6 rounded-xl shadow-xl bg-base-green font-bold text-white transform hover:scale-110 hover:opacity-80">
          Admin
        </span>
      </Link>
    </div>
  );
};

export default IndexPage;
