import Head from "next/head";

import { Layout } from "../../../components/shared";
import { RegisteredProject } from "../../../components/join-us/maintainer/registered-project";

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
        <RegisteredProject />
      </Layout>
    </>
  );
};

export default ContributorPage;
