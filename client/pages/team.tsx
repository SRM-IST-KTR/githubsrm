import { GetStaticPropsResult } from "next";
import Head from "next/head";
import { Layout } from "../components/shared/index";
import { Team } from "../components/team";
import { MemberProps } from "../utils/interfaces";
import { getTeam } from "../services/api";

interface TeamPageProps {
  team: MemberProps[];
}

const TeamPage = ({ team }: TeamPageProps) => {
  return (
    <div>
      <Head>
        <title>GitHub Community SRM | Team</title>
        <meta
          name="description"
          content="A team of 11 students of SRMIST trying to spearhead open-source revolution in SRMIST through the GitHub Community SRM"
        />
      </Head>
      <Layout>
        <Team team={team} />
      </Layout>
    </div>
  );
};

export default TeamPage;

export const getStaticProps = async (): Promise<
  GetStaticPropsResult<TeamPageProps>
> => {
  try {
    const res = await getTeam();
    if (res) {
      return {
        props: { team: res as MemberProps[] },
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
    return {
      redirect: {
        permanent: false,
        destination: "/500",
      },
    };
  }
};
