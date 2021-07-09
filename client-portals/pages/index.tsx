import Link from "next/link";

const IndexPage = () => {
  return (
    <div>
      <Link href="/maintainer">maintainer</Link>
      <Link href="/admin">admin</Link>
    </div>
  );
};

export default IndexPage;
