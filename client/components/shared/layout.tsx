import { useRef } from "react";
import { useRouter } from "next/router";
import { motion, useElementScroll, useTransform } from "framer-motion";

import { Navbar } from "./";
import { OSS, Team } from "../../utils/titles";

const Layout: React.FC = ({ children }) => {
  const { pathname } = useRouter();
  const scrollDivRef = useRef<HTMLDivElement>();
  const { scrollYProgress } = useElementScroll(scrollDivRef);
  const opacity = useTransform(scrollYProgress, [0, 0.2], [1, 0]);

  return (
    <>
      <div className="fixed w-full h-screen bg-gradient-to-b from-base-blue to-base-black -z-10" />
      <div className="flex flex-col w-11/12 h-screen pt-16 mx-auto">
        <Navbar />

        {/* scrollable */}
        <div
          ref={scrollDivRef}
          className="w-full relative mx-auto h-full bg-base-black overflow-scroll no-scrollbar"
        >
          <motion.figure
            className="flex sticky top-0 justify-center w-full px-12"
            style={{ opacity }}
          >
            {pathname === "/" ? <OSS /> : <Team />}
          </motion.figure>

          <div className="absolute w-full top-0 z-10">
            <div className="w-11/12 mx-auto bg-white mt-80 mb-10 p-10 overflow-auto rounded-2xl">
              {children}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Layout;
