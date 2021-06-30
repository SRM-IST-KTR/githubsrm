import { motion, useViewportScroll, useTransform } from "framer-motion";

import { CoderOcto } from "../../utils/icons";

const Hero = () => {
  const { scrollYProgress } = useViewportScroll();
  const y = useTransform(scrollYProgress, [0, 0.15], [1, 0]);

  const messages: string[] = [
    "We plan on administrating the SRMIST KTR GitHub Enterprise Organisation.",
    "Help the faculties in managing and maintaining student projects.",
    "Help the students get onboard with their projects under the SRMIST KTR GitHub Enterprise.",
  ];

  return (
    <div className="pb-10 lg:mt-20 lg:mb-20">
      <div className="grid grid-cols-1 lg:grid-cols-3 items-center">
        <div className="text-xl z-40 mb-10 lg:mb-0 w-full">
          <motion.h1
            style={{ y: y }}
            className="flex z-40 justify-center text-base-blue text-4xl md:text-5xl xl:text-6xl font-extrabold mb-6"
          >
            GitHub Community SRM
          </motion.h1>
          <p className="w-full text-gray-600 font-regular text-sm lg:text-lg">
            GitHub Community SRM is the official student-led community
            spearheading the Open Source Revolution at SRMIST, Chennai.
          </p>
        </div>

        <div className="flex justify-items-center z-10 items-center flex-col">
          <div className="absolute rounded-full bg-base-blue bg-opacity-70 p-28 md:p-32 lg:p-48" />
          <motion.div
            animate={{ y: 100 }}
            transition={{
              repeat: Infinity,
              repeatType: "reverse",
              duration: 2,
            }}
          >
            <div className="w-56 lg:w-96 z-50 -mt-10 mb-14">
              <CoderOcto />
            </div>
          </motion.div>
        </div>

        <div className="grid grid-rows-3 gap-2 w-full mt-10 lg:mt-0 lg:p-7">
          {messages.map((message, index) => (
            <div
              key={message}
              className={`${
                index % 2 ? "lg:ml-20" : ""
              } lg:my-5 flex flex-col justify-center items-stretch lg:items-center`}
            >
              <p className="lg:text-center p-2 lg:py-4 font-medium text-gray-100 bg-base-green rounded-2xl">
                {message}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Hero;
