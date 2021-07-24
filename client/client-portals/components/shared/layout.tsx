import React from "react";
import Navbar from "./navbar";
import { AuthContext } from "context/authContext";
import Footer from "./footer";

const admin_links = [
  {
    link: "/admin/dashboard",
    name: "Projects",
  },
  {
    link: "/admin/dashboard/accepted-projects",
    name: "Contributors",
  },
];

const maintainer_links = [
  {
    link: "/maintainer/dashboard",
    name: "My Projects",
  },
  {
    link: "/maintainer/reset-password/reset",
    name: "Reset Password",
  },
];

export default function Layout({ type, children }) {
  const authContext = React.useContext(AuthContext);
  return (
    <div className="flex flex-col justify-between bg-base-blue min-h-screen w-full">
      {authContext.isAuth && (
        <Navbar links={type === "admin" ? admin_links : maintainer_links} />
      )}
      <div className="p-10 pt-24 w-full">{children}</div>
      <div className="w-full mx-auto mb-0">
        <Footer />
      </div>
    </div>
  );
}
