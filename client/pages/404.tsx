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
        src="https://assets1.lottiefiles.com/temp/lf20_dzWAyu.json"
      />
    </Layout>
  );
};

export default NotFound;
