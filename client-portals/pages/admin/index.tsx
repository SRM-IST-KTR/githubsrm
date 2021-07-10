import Link from "next/link";

const IndexPage = () => {
  return (
    <div>
      <Link href="/admin/register">register</Link>
      <Link href="/admin/login">login</Link>
    </div>
  );
};

export default IndexPage;
