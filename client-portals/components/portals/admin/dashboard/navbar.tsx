import Link from "next/link";

const Adminnavbar = () => {
  return (
    <div className="flex flex-row justify-center text-white my-6">
      <div className="mx-2 text-xl p-3  border-b-4 border-base-teal">
        <Link href="/admin/dashboard">Project Dashboard</Link>
      </div>
      <div className="mx-2 text-xl p-3 border-b-4 border-base-teal">
        <Link href="/admin/dashboard/accepted-projects">Accepted Projects</Link>
      </div>
    </div>
  );
};

export default Adminnavbar;
