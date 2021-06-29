import { Layout } from "../components/shared/index";
import { Player } from "@lottiefiles/react-lottie-player";

const NotFound = () => {
  return (
    <Layout>
      <Player
        background="transparent"
        speed={1}
        className="w-full md:w-1/3"
        loop
        autoplay
        src="https://assets3.lottiefiles.com/packages/lf20_dF0drO.json"
      />
    </Layout>
  );
};

export default NotFound;
