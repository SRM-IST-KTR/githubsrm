import { motion, useViewportScroll, useTransform } from "framer-motion";
import { CoderOcto } from "../../utils/icons";
import Tilt from "react-tilt";

interface HeroProps {
  reference?: HTMLDivElement;
}

const Hero = ({ reference }: HeroProps) => {
  const { scrollYProgress } = useViewportScroll();
  const y = useTransform(scrollYProgress, [0, 0.15], [1, 0]);

  return (
    <div>
      <div className="pb-10 lg:mt-20 lg:mb-32">
        <div className="grid grid-cols-1 xl:grid-cols-3 items-center mx-2">
          <div className="text-xl z-40 ">
            <motion.h1
              style={{ y: y }}
              className="flex z-40  justify-center text-base-blue text-4xl lg:text-6xl font-extrabold mb-6"
            >
              GitHub Community SRM
            </motion.h1>
            <p className="text-gray-600 font-regular text-sm lg:text-lg">
              GitHub Community SRM is the official student-led community
              spearheading the Open Source Revolution at SRMIST, Chennai.
            </p>
            <br />
          </div>
          <div className="flex justify-items-center z-10 items-center flex-col">
            <div className="absolute rounded-full bg-base-blue p-28 md:p-32 lg:p-48 "></div>
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

          <div className="grid grid-rows-3 w-full lg:p-7">
            <Tilt className="Tilt cursor-default" options={{ max: 25 }}>
              <div className="my-1 lg:my-5 bg-base-green rounded-2xl flex justify-center items-center flex-col">
                <p className="text-center mx-2 p-1 lg:p-2 font-semibold text-gray-100">
                  We plan on administering the SRMIST KTR GitHub Enterprise
                  organization
                </p>
              </div>
            </Tilt>
            <Tilt className="Tilt cursor-default" options={{ max: 25 }}>
              <div className="my-1 lg:my-5 lg:ml-20 bg-base-teal  rounded-2xl flex justify-center items-center flex-col">
                <p className="text-center mx-2 p-1 lg:p-2 font-semibold text-gray-100">
                  Help the faculties in managing and maintaining student
                  projects
                </p>
              </div>
            </Tilt>
            <Tilt className="Tilt cursor-default" options={{ max: 25 }}>
              <div className="my-1 lg:my-5 bg-base-green  rounded-2xl flex justify-center items-center flex-col">
                <p className="text-center mx-2 p-1 lg:p-2 font-semibold text-gray-100">
                  Help the students get onboarded and get started with their
                  major,minor and personal projects under the SRMIST KTR GitHub
                  Enterprise.
                </p>
              </div>
            </Tilt>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
