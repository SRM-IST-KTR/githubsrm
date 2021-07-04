import { Layout } from "../../components/shared";
import { JoinUs } from "../../components/join-us";
import Head from "next/head";

const JoinUsPage = () => {
  return (
    <div>
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
    </div>
  );
};

export default JoinUsPage;
