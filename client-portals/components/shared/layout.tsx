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
    link: "/admin/dashboard/profile/",
    name: "My Profile",
  },
];

export default function Layout({ type, children }) {
  return (
    <div className="min-h-screen p-10 bg-base-blue w-full">
      <Navbar links={type === "admin" ? admin_links : maintainer_links} />
      {children}
    </div>
  );
}
