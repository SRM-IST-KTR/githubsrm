import { GetServerSidePropsResult } from "next";

import { Layout } from "../../components/shared";
import { Contributor } from "../../components/join-us/contributor";

interface ContributorPageProps {
  selectProjects: { value: string; name: string }[];
}

const ContributorPage = ({ selectProjects }: ContributorPageProps) => {
  return (
    <Layout>
      <Contributor projectOption={selectProjects} />
    </Layout>
  );
};

export default ContributorPage;

export const getServerSideProps = async (): Promise<
  GetServerSidePropsResult<ContributorPageProps>
> => {
  try {
    return {
      props: {
        selectProjects: [
          { name: "GitHubSRM Landing", value: "githubsrm-landing" },
          { name: "Ossmosis", value: "ossmosis" },
        ],
      },
    };
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
