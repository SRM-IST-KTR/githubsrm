import Link from "next/link";
import { Player } from "@lottiefiles/react-lottie-player";

import { Layout } from "../components/shared/index";

const NotFound = () => {
  return (
    <Layout>
      <Player
        background="transparent"
        speed={1}
        className="w-full md:w-1/3"
        loop
        autoplay
        src="/lottie/server-error.json"
      />
      <div className="text-center mt-6 text-lg">
        Click{" "}
        <Link href="/">
          <a className="font-semibold hover:underline text-base-blue">here</a>
        </Link>{" "}
        to go back!
      </div>
    </Layout>
  );
};

export default NotFound;
