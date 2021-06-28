import { GetServerSidePropsResult } from "next";

import { Layout } from "../components/shared/index";
import { Team } from "../components/team";
import { MemberProps } from "../utils/interfaces";
import { getTeam } from "../services/api";

interface TeamPageProps {
  team: MemberProps[];
}

const TeamPage = ({ team }: TeamPageProps) => {
  return (
    <Layout>
      <Team team={team} />
    </Layout>
  );
};

export default TeamPage;

export const getServerSideProps = async (): Promise<
  GetServerSidePropsResult<TeamPageProps>
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
    console.log(error);
    return {
      redirect: {
        permanent: false,
        destination: "/500",
      },
    };
  }
};
