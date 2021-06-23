import { Player } from "@lottiefiles/react-lottie-player";

import { Soon, Socials } from "./";

const Hero = () => {
  return (
    <div className="flex flex-col w-screen h-screen bg-secondary justify-center items-center text-primary">
      <Player
        src="https://assets9.lottiefiles.com/packages/lf20_S6vWEd.json"
        background="transparent"
        speed={1}
        className="w-64 md:w-96"
        loop
        autoplay
      />

      <Soon />

      <Socials />
    </div>
  );
};

export default Hero;
