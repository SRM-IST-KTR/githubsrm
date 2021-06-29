import {
  GitHubIcon,
  TwitterIcon,
  InstagramIcon,
  LinkedinIcon,
} from "../../utils/icons";
import { motion } from "framer-motion";

const Footer = () => {
  const socials: {
    icon: JSX.Element;
    href: string;
  }[] = [
    {
      icon: <GitHubIcon />,
      href: "https://github.com/srm-ist-ktr",
    },
    {
      icon: <TwitterIcon />,
      href: "https://twitter.com/githubsrm",
    },
    {
      icon: <LinkedinIcon />,
      href: "https://www.linkedin.com/company/githubsrm/mycompany/",
    },
    {
      icon: <InstagramIcon />,
      href: "https://www.instagram.com/githubsrm/",
    },
  ];

  return (
    <div className="bg-base-smoke flex flex-col md:flex-row justify-evenly items-center rounded-b-2xl p-2 md:p-6 text-white">
      <div className="w-1/3 h-0 md:h-auto text-base-blue font-medium">
        <a href="mailto:community@githubsrm.tech">community@githubsrm.tech</a>
      </div>
      <p className="w-full md:w-1/3 text-center my-2 md:my-auto text-gray-700 font-regular mx-2 min-w-max">
        Developed with <span className="line-through">friends</span> Groovy
        &hearts;
      </p>
      <div className="w-full md:w-1/3 flex flex-row justify-around md:justify-evenly items-center">
        {socials.map((social) => (
          <motion.div
            key={social.href}
            whileHover={{ scale: 1.2, rotate: 360 }}
            whileTap={{ scale: 1.3, rotate: -360, borderRadius: "100%" }}
          >
            <a
              href={social.href}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-base-teal flex justify-center items-center p-2 rounded-xl"
            >
              <span className="w-5 h-5">{social.icon}</span>
            </a>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Footer;
