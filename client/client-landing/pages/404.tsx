import Link from "next/link";
import Head from "next/head";
import { Player } from "@lottiefiles/react-lottie-player";

import { Layout } from "../components/shared/index";

const NotFound = () => {
  return (
    <>
      <Head>
        <title>GitHub Community SRM | Not Found</title>
        <meta
          name="description"
          content="A team of 11 students of SRMIST trying to spearhead open-source revolution in SRMIST through the GitHub Community SRM"
        />
      </Head>
      <Layout>
        <Player
          background="transparent"
          speed={1}
          className="w-full md:w-1/3"
          loop
          autoplay
          src="/lottie/not-found.json"
        />
        <div className="text-center mt-6 text-lg">
          Click{" "}
          <Link href="/">
            <a className="font-semibold hover:underline text-base-blue">here</a>
          </Link>{" "}
          to go back!
        </div>
      </Layout>
    </>
  );
};

export default NotFound;
