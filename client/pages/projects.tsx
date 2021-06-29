import { GetStaticPropsResult } from "next";

import { Layout } from "../components/shared";
import { ProjectProps } from "../utils/interfaces";
import { Projects } from "../components/projects";
import { getProjects } from "../services/api";

interface TeamPageProps {
  projects: ProjectProps[];
}

const ProjectsPage = ({ projects }: TeamPageProps) => {
  return (
    <Layout>
      <Projects projects={projects} />
    </Layout>
  );
};

export default ProjectsPage;

export const getStaticProps = async (): Promise<
  GetStaticPropsResult<TeamPageProps>
> => {
  try {
    const res = await getProjects();
    if (res) {
      return {
        props: { projects: res as ProjectProps[] },
      };
    } else {
      return {
        redirect: {
          permanent: false,
          destination: "/500",
        },
      };
    }
  } catch (error) {
    console.log(error);
    return {
      redirect: {
        permanent: false,
        destination: "/500",
      },
    };
  }
};
