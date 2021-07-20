import Head from "next/head";

import { Layout } from "../../../components/shared";
import { Maintainer } from "../../../components/join-us/maintainer";

const ContributorPage = () => {
  return (
    <>
      <Head>
        <title>GitHub Community SRM | Join Us | Maintainer</title>
        <meta
          name="description"
          content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
        />
      </Head>
      <Layout>
        <Maintainer />
      </Layout>
    </>
  );
};

export default ContributorPage;
