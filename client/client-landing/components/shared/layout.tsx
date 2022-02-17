import { useRef } from "react";
import { useRouter } from "next/router";
import { motion, useElementScroll, useTransform } from "framer-motion";

import { Navbar, Footer } from ".";
import * as Titles from "../../utils/titles";

const Layout: React.FC = ({ children }) => {
  const { pathname } = useRouter();
  const scrollDivRef = useRef<HTMLDivElement>();
  const { scrollYProgress } = useElementScroll(scrollDivRef);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.95], [1, 0.5, 0.25]);
  const YText = useTransform(scrollYProgress, [0, 0.8], ["0%", "10%"]);
  const YCard = useTransform(scrollYProgress, [0, 0.8], ["0%", "-5%"]);

  const Title = () => {
    switch (pathname) {
      case "/": {
        return <Titles.OSS />;
      }
      case "/team": {
        return <Titles.Team />;
      }
      case "/join-us": {
        return <Titles.JoinUs />;
      }
      case "/join-us/maintainer/existing-project":
      case "/join-us/maintainer/new-project":
      case "/join-us/maintainer":
      case "/join-us/contributor":
      case "/join-us": {
        return <Titles.JoinUs />;
      }
      case "/projects": {
        return <Titles.Projects />;
      }
      case "/contact-us": {
        return <Titles.Contact />;
      }
      case "/documentation": {
        return "Documentation Svg Template";
      }
      case "/500": {
        return <Titles.ServerError />;
      }
      default: {
        return <Titles.ErrorPage />;
      }
    }
  };

  return (
    <>
      <div className="fixed w-full h-screen bg-gradient-to-b from-base-blue to-base-black -z-10" />
      <div className="flex flex-col w-11/12 h-screen pt-4 lg:pt-12 mx-auto">
        <Navbar />

        {/* * INFO: scrollable div below */}
        <div
          ref={scrollDivRef}
          className="w-full relative mx-auto h-full bg-base-black overflow-scroll no-scrollbar rounded-t-2xl pt-8"
        >
          <motion.figure
            className="flex sticky top-0 justify-center w-full px-6 lg:px-12"
            style={{ opacity, y: YText }}
          >
            {Title()}
          </motion.figure>

          <motion.div
            style={{ y: YCard }}
            className="absolute w-full top-0 z-10"
          >
            <div className="w-11/12 mx-auto bg-white mt-36 lg:mt-80 px-4 py-10 md:p-10 overflow-auto rounded-t-md lg:rounded-t-2xl">
              <div className="max-w-9xl mx-auto">{children}</div>
            </div>
            <div className="w-11/12 mx-auto mb-10">
              <Footer />
            </div>
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default Layout;
