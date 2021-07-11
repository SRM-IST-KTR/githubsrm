import Link from "next/link";

const IndexPage = () => {
  return (
    <div className="min-h-screen bg-base-blue flex flex-col justify-center items-center">
      <Link href="/maintainer">
        <span className="py-7 cursor-pointer hover:opacity-50 px-16 rounded-xl shadow-xl bg-base-green text-gray-100 font-bold">
          {" "}
          maintainer
        </span>
      </Link>
      <Link href="/admin">
        <span className="py-7 cursor-pointer hover:opacity-50 px-20 mt-6 rounded-xl shadow-xl bg-base-green text-gray-100 font-bold">
          admin
        </span>
      </Link>
    </div>
  );
};

export default IndexPage;
