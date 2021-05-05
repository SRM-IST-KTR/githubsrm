import { GetServerSidePropsResult } from "next";

const NotFound = () => {
  return <></>;
};

export default NotFound;

export async function getServerSideProps(): Promise<
  GetServerSidePropsResult<{}>
> {
  try {
    return { redirect: { destination: "/", permanent: false } };
  } catch (err) {
    return { redirect: { destination: "/", permanent: false } };
  }
}
