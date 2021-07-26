import { Layout } from "@/shared/index";
import { ErrorPage } from "@/icons/index";

const NotFound = () => {
  return (
    <>
      <Layout type="admin">
        <ErrorPage />
      </Layout>
    </>
  );
};

export default NotFound;
