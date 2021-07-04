import Head from "next/head";

import { Layout } from "../../components/shared";
import { Contributor } from "../../components/join-us/contributor";

const ContributorPage = () => {
  return (
    <>
      <Head>
        <title>GitHub Community SRM | Join Us | Contributor</title>
        <meta
          name="description"
          content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
        />
      </Head>
      <Layout>
        <Contributor />
      </Layout>
    </>
  );
};

export default ContributorPage;
