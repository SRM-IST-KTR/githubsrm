import Head from "next/head";

import { Layout } from "../components/shared/index";
import { Team } from "../components/team";

const TeamPage = () => {
  return (
    <>
      <Head>
        <title>GitHub Community SRM | Team</title>
        <meta
          name="description"
          content="A team of passionate student developers of SRMIST trying to spearhead open-source revolution in SRMIST through the GitHub Community SRM"
        />
      </Head>
      <Layout>
        <Team />
      </Layout>
    </>
  );
};

export default TeamPage;
