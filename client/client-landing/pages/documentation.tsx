import Head from "next/head";

import { Documentation } from "../components/documentation";
import { Layout } from "../components/shared";

const documentation = () => {
  return (
    <>
      <Head>
        <title>Documentation</title>
        <meta
          name="documentation"
          content="GitHub Community SRM aims to help teachers manage student projects on the SRMIST KTR GitHub Enterprise"
        />
      </Head>
      <Layout>
        <Documentation />
      </Layout>
    </>
  );
};

export default documentation;
