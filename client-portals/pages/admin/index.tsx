import Link from "next/link";

const IndexPage = () => {
  return (
    <div className="flex justify-center items-center h-screen text-white bg-base-blue">
      <div className="bg-base-green text-xl p-2 mx-2 rounded">
        <Link href="/admin/register">Register</Link>
      </div>
      <div className="bg-base-green text-xl p-2 mx-2 rounded">
        <Link href="/admin/login">Login</Link>
      </div>
    </div>
  );
};

export default IndexPage;
