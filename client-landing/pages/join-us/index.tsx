import Head from "next/head";

import { Layout } from "../../components/shared";
import { JoinUs } from "../../components/join-us";

const JoinUsPage = () => {
  return (
    <>
      <Head>
        <title>GitHub Community SRM | Join Us</title>
        <meta
          name="description"
          content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
        />
      </Head>
      <Layout>
        <JoinUs />
      </Layout>
    </>
  );
};

export default JoinUsPage;
