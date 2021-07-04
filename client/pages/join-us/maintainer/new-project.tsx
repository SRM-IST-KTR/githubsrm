import Head from "next/head";

import { Layout } from "../../../components/shared";
import { NewProject } from "../../../components/join-us/maintainer/new-project";

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
        <NewProject />
      </Layout>
    </>
  );
};

export default ContributorPage;
