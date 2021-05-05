import { GetStaticPropsResult } from "next";

const NotFound = () => {
  return <></>;
};

export default NotFound;

export async function getStaticProps(): Promise<GetStaticPropsResult<{}>> {
  try {
    return { redirect: { destination: "/", permanent: false } };
  } catch (err) {
    return { redirect: { destination: "/", permanent: false } };
  }
}
