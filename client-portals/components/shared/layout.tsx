import Navbar from "./navbar";

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
    link: "/maintainer/dashboard/reset-password/reset",
    name: "Reset Password",
  },
  {
    link: "/maintainer/dashboard/reset-password/set",
    name: "Set Password",
  },
];

export default function Layout({ type, children }) {
  return (
    <div className="bg-base-blue">
      <Navbar links={type === "admin" ? admin_links : maintainer_links} />
      <div className="min-h-screen p-10  w-full">{children}</div>
    </div>
  );
}
