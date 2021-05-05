import { Player } from "@lottiefiles/react-lottie-player";

import { Soon } from "./";

const Hero = () => {
  return (
    <div className="flex flex-col w-screen h-screen bg-secondary justify-center items-center text-primary">
      <Player
        src="https://assets9.lottiefiles.com/packages/lf20_S6vWEd.json"
        background="transparent"
        speed={1}
        className="w-96 h-96"
        loop
        autoplay
      />

      <Soon />
    </div>
  );
};

export default Hero;
