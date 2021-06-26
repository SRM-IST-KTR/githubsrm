import { useRef } from "react";
import { useRouter } from "next/router";
import { motion, useElementScroll, useTransform } from "framer-motion";

import { Navbar } from "../components/shared";
import { OSS, Team, JoinUs, Projects } from "../utils/titles";

const NotFound = () => {
  const { pathname } = useRouter();
  const scrollDivRef = useRef<HTMLDivElement>();
  const { scrollYProgress } = useElementScroll(scrollDivRef);
  const opacity = useTransform(scrollYProgress, [0, 0.15], [1, 0]);
  const Y = useTransform(scrollYProgress, [0, 0.2], [0, 100]);

  return (
    <>
      <div className="fixed w-full h-screen bg-gradient-to-b from-base-blue to-base-black -z-10" />
      <div className="flex flex-col w-11/12 h-screen pt-16 mx-auto">
        <Navbar />

        {/* scrollable */}
        <div
          ref={scrollDivRef}
          className="w-full relative mx-auto h-full bg-base-black overflow-scroll no-scrollbar text-9xl font-extrabold text-base-smoke text-center "
        >
          <span>4</span>
          <span>0</span>
          <span>4</span>
        </div>
      </div>
    </>
  );
};

export default NotFound;
