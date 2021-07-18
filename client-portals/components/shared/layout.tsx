import React from "react";
import Navbar from "./navbar";
import { AuthContext } from "../../context/authContext";

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
    <div className="bg-base-blue">
      {authContext.isAuth && (
        <Navbar links={type === "admin" ? admin_links : maintainer_links} />
      )}
      <div className="min-h-screen p-10 w-full">{children}</div>
    </div>
  );
}
