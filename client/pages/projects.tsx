import { Layout } from "../components/shared";
import Head from "next/head";
import { Projects } from "../components/projects";

const ProjectsPage = () => {
  return (
    <div>
      <Head>
        <title>GitHub Community SRM | Projects</title>
        <meta
          name="description"
          content="GitHub Community SRM aims to help teachers manage student projects on the SRMIST KTR GitHub Enterprise"
        />
      </Head>
      <Layout>
        <Projects />
      </Layout>
    </div>
  );
};

export default ProjectsPage;
